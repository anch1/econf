CREATE TABLE public.section
(
  id_section integer NOT NULL,
  id_application integer,
  "NameSection" character varying(250),
  id_member integer,
  CONSTRAINT pk_section PRIMARY KEY (id_section)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.section
  OWNER TO pi;