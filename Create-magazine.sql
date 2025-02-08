-- Table: public.magazines

-- DROP TABLE IF EXISTS public.magazines;

CREATE TABLE IF NOT EXISTS public.magazines
(
    id integer NOT NULL DEFAULT nextval('magazines_id_seq'::regclass),
    title text COLLATE pg_catalog."default" NOT NULL,
    author text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    publication_date text COLLATE pg_catalog."default",
    CONSTRAINT magazines_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.magazines
    OWNER to postgres;
-- Index: idx_fulltext

-- DROP INDEX IF EXISTS public.idx_fulltext;

CREATE INDEX IF NOT EXISTS idx_fulltext
    ON public.magazines USING gin
    (to_tsvector('english'::regconfig, (((title || ' '::text) || author) || ' '::text) || category))
    TABLESPACE pg_default;
