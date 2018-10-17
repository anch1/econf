CREATE TABLE public.conf
(
  id_conf bigint NOT NULL DEFAULT nextval('conf_id_conf_seq'::regclass),
  "StatusConf" integer, -- 0 - создана...
  id_application integer,
  theme character varying(250),
  id_company integer,
  id_sciency integer,
  datefrom date,
  dateto date,
  dateatticle date,
  datedecision date,
  describe_conf character varying(2096),
  orgcom_conf character varying, -- 2096
  CONSTRAINT pk_conf PRIMARY KEY (id_conf)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.conf
  OWNER TO pi;
COMMENT ON COLUMN public.conf."StatusConf" IS '0 - создана
1 - размещение материала
2 -открытая конференция
3 - закрыто обсуждение';
COMMENT ON COLUMN public.conf.orgcom_conf IS '2096';

-- Table: public.moderators

-- DROP TABLE public.moderators;

CREATE TABLE public.moderators
(
  id_moderator integer,
  id_member integer,
  id_conf integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.moderators
  OWNER TO pi;
