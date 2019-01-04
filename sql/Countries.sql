create table country
(
id int,
fullname character varying(250),
name character varying(250),
fullnameeng character varying(250),
nameeng character varying(250),
isonum int,
iso2 character(5),
iso3 character(5)
);

COPY country FROM '/home/pi/PycharmProjects/econf/sql/c1.csv' DELIMITER ';' CSV;

ALTER TABLE public.members ADD COLUMN id_country int;