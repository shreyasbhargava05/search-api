-- View: public.magazine_search_view

-- DROP MATERIALIZED VIEW IF EXISTS public.magazine_search_view;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.magazine_search_view
TABLESPACE pg_default
AS
 SELECT m.id,
    m.title,
    m.author,
    m.publication_date,
    m.category,
    mc.content,
    mc.vector_representation,
    to_tsvector('english'::regconfig, (((((m.title || ' '::text) || m.author) || ' '::text) || m.category) || ' '::text) || mc.content) AS text_col
   FROM magazines m
     JOIN magazine_contents mc ON m.id = mc.magazine_id
WITH DATA;

ALTER TABLE IF EXISTS public.magazine_search_view
    OWNER TO postgres;

CREATE UNIQUE INDEX idx_magazine_search_view_id
ON public.magazine_search_view(text_col);


CREATE INDEX magazine_search_view_idx
    ON public.magazine_search_view USING btree
    (text_col)
    TABLESPACE pg_default;
