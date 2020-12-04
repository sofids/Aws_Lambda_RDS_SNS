# Aws_Lambda_RDS_SNS
Proyecto de Aws de envío de notificaciones SNS a clientes sobre una película recomendada a partir del disparador de la carga de archivos en S3 y actualización de la bd RDS Mysql
### Objetivo
 Desarrollar un proyecto de AWS integrando diferentes servicios.

### Tecnologías a usar
- AWS: Proveedor cloud
- MySql: base de datos relacional


### Archivos de Datos
 Se usará el siguiente CSV:
 movies.csv: Contiene una lista de películas con sus atributos(título, actores, calificación, año de estreno,etc)

### Pre requisitos
- Tener una cuenta en AWS
- Tener instalado un cliente MySql en local

### Desarrollo
1. Configurar los roles y políticas necesarias en el IAM
2. Crear un bucket en S3
3. Configurar una base de datos RDS Mysql
4. Configurar el cliente Mysql en local leyendo el RDS Mysql a fin de tener una interfaz para ejecutar querys.
5. Configurar una notificación SNS por email y una suscripción
6. Crear una función lambda que se dispare cuando se coloque el archivo movies.csv en el S3. 
    El archivo debe usarse para insertar nuevos registros en la base de datos
    RDS Mysql. Luego debe hallarse la película top según la que tenga mayor calificación de los usuarios.
    Dicha película se usará para armar el correo a ser enviado por SNS a los suscriptores.
7. Generar reportes en Quicksight leyendo la base de datos RDS MySql

  
