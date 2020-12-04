select * from movies;

select count(*) from movies;

#registros del csv
SELECT * FROM movies where title in 
('The Avengers','Good Will Hunting','2001: A Space Odyssey','Scarface',
'Gran Torino','Three Billboards Outside Ebbing Missouri','A Beautiful Mind','Fargo',
'Vertigo','Blade Runner','Before Sunrise','Fiddler on the Roof','The Night of the Hunter',
'My Name Is Khan','To Be or Not to Be');

#nueva pelicula top
select title, actors,description,genre,
runtime,year, imdb_url ,rating from movies order by users_rating desc limit 1