CREATE TABLE public.conf
(
  id_conf bigint NOT NULL DEFAULT nextval('conf_id_conf_seq'::regclass),
  "StatusConf" integer, -- 0 - создана...
  id_application integer,
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

