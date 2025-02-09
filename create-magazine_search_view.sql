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



-- For vector search
CREATE INDEX idx_vector_representation ON magazine_search_view USING hnsw (vector_representation vector_l2_ops);

-- For full-text search
CREATE INDEX idx_text_col ON magazine_search_view USING gin (text_col);


