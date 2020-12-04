import json
import botocore
import boto3
import logging
import os
import sys
import uuid
import pymysql
import csv
import rds_config

#credenciales de bd
db_host  = rds_config.db_host
db_username = rds_config.db_username#
db_password = rds_config.db_password
db_name = rds_config.db_name

#conectando a la base de datos
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(db_host, user=db_username, passwd=db_password, db=db_name, connect_timeout=5)
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

#funcion que inserta un registro en la tabla movies 
def inserta_new_movies(row_insert):
    try: 
        with conn.cursor() as cur:
            cur.execute('INSERT INTO movies (title,rating,year,users_rating,votes,metascore,img_url,countries,languages,'\
            'actors,genre,tagline,description,directors,runtime,imdb_url)values (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s,%s,%s, %s,%s,%s)',row_insert)
            conn.commit()
    except Exception as e:
        logger.error(e)
    return "ok new movies"
#funcion que obtiene la pelicula top 
def top_movie():
    with conn.cursor() as cur:
        cur.execute("select title, actors,description,genre,runtime,year, imdb_url ,rating from movies order by users_rating desc limit 1")
        for row in cur:
            titulo=row[0]
            actores=row[1]
            descripcion=row[2]
            genero=row[3]
            duracion=row[4]
            anio=row[5]
            link=row[6]
            calificacion=row[7]
            correo="Le recomendamos ver la pelicula "+titulo+"("+str(anio)+")|"+calificacion+"|"+str(duracion)+"|"+genero+"|"+actores+":"+descripcion+" Veala en:"+link
            logger.info(correo)
    return correo

def envia_email(mensaje,topico,asunto):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=topico,
        Message=mensaje,
        Subject=asunto,
        MessageStructure='raw'
          )
    return "Mensaje enviado"

def lambda_handler(event, context):
  s3_client = boto3.client('s3')
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = event['Records'][0]['s3']['object']['key'] 
  download_path = '/tmp/'+key
  print(download_path,bucket,key)
  s3_client.download_file(bucket, key,download_path)
  with open(download_path) as csvfile:
      reader = csv.DictReader(csvfile, delimiter=';')
      rowCount = 0
      for row in reader:
          rowCount += 1
          print(row['title'], row['year'], row['votes'])
          row_insert=(row['title'],row['rating'], row['year'], row['users_rating'],row['votes'],row['metascore'],row['img_url'],row['countries'],
                      row['languages'],row['actors'],row['genre'],row['tagline'], row['description'],row['directors'],row['runtime'],row['imdb_url'])
          inserta_new_movies(row_insert)
  topico="arn:aws:sns:us-east-2:762011018360:top_movies"
  asunto='Pelicula Top del dia en IMDB'
  mensaje=top_movie()
  print(mensaje)
  envia_email(mensaje,topico,asunto)
  return 'Se insertaron'+str(rowCount)+" registros en la tabla movies"
  