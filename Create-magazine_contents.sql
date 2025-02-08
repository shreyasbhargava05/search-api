-- Table: public.magazine_contents

-- DROP TABLE IF EXISTS public.magazine_contents;

CREATE TABLE IF NOT EXISTS public.magazine_contents
(
    id integer NOT NULL,
    magazine_id integer,
    content text COLLATE pg_catalog."default",
    vector_representation vector(768),
    CONSTRAINT magazine_contents_pkey PRIMARY KEY (id),
    CONSTRAINT magazine_contents_magazine_id_fkey FOREIGN KEY (magazine_id)
        REFERENCES public.magazines (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.magazine_contents
    OWNER to postgres;
-- Index: idx_content_fulltext

-- DROP INDEX IF EXISTS public.idx_content_fulltext;

CREATE INDEX IF NOT EXISTS idx_content_fulltext
    ON public.magazine_contents USING gin
    (to_tsvector('english'::regconfig, content))
    TABLESPACE pg_default;
