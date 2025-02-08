from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
import psycopg2
from psycopg2.extras import execute_values, execute_batch  # For bulk insert (if needed)
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI()

# Database connection details (replace with your credentials)
DATABASE_URL = "postgresql://postgres:root@localhost:5432/vectordb"

# Initialize the sentence transformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Dependency to get a database connection
def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    finally:
        if conn:
            conn.close()

@app.post("/search")
async def search(
    query: str,
    limit: int = 10,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    cursor = db.cursor()
    keyword_sql = ""
    try:
        
        # Keyword Search: Search based on keywords in the title, author, category and content
        
        keyword_sql = f"""
            SELECT id, title, author, category, content, ts_rank(text_col, phraseto_tsquery('english', '{query}') ) AS keyword_relevance
            FROM magazine_search_view
            WHERE text_col @@ phraseto_tsquery('english', '{query}')
            order by ts_rank(text_col, phraseto_tsquery('english', '{query}') )  LIMIT {limit}
        """
        cursor.execute(keyword_sql)
        keyword_results = {row[0]: row for row in cursor.fetchall()} # Store results in a dictionary for faster lookup

        # Vector Search: Search based on vector similarity in the vector_representation field
        
        vector = model.encode(query)
        embadding = vector.tolist()
        vector_sql = f"""
            SELECT mv.id, mv.title, mv.author, mv.category, mv.content
            FROM magazine_search_view mv           
            ORDER BY mv.vector_representation <-> '{embadding}' LIMIT {limit}
        """
        cursor.execute(vector_sql)
        vector_results = {row[0]: row for row in cursor.fetchall()} # Store results in a dictionary
        
        # Hybrid Search: Hybrid Search: Combine the results of both keyword and vector searches to return the most relevant results
        combined_results = {}
        for id, keyword_row in keyword_results.items():
            combined_results[id] = {
                "id": keyword_row[0], "title": keyword_row[1], "author": keyword_row[1], "category": keyword_row[2], "content": keyword_row[3],
                "keyword_relevance": keyword_row[4]
            }

        for id, vector_row in vector_results.items():
            if id not in combined_results:
                combined_results[id] = {
                    "id": vector_row[0],"title": vector_row[1], "author": vector_row[1], "category": vector_row[2], "content": vector_row[3]
                }

        return {"results": combined_results}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        cursor.close()



@app.post("/update_vectors")
async def update_vectors(db: psycopg2.extensions.connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        # 1. Fetch records needing updates (using the correct check for empty vectors)
        cursor.execute("""
            SELECT id, content 
            FROM magazine_contents 
            WHERE content IS NOT NULL AND (vector_representation IS NULL OR array_length(vector_representation::real[], 1) IS NULL)
        """)
        records_to_update = cursor.fetchall()

        if not records_to_update:
            return {"message": "No records needed vector update."}

        vectors_to_update = []
        for record_id, content in records_to_update:
            try:
                vector = model.encode(content)
                print(f"Vector dimension: {len(vector)}")  # Check the dimension    

                # Check if the encoded vector has at least one dimension.
                if len(vector) == 0:
                    print(f"Warning: Empty vector generated for record ID {record_id}. Skipping.")
                    continue
                vector_list = vector.tolist()  # Or tuple(vector)
                vectors_to_update.append((vector_list, record_id))  # Keep as tuples

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error encoding content for record ID {record_id}: {e}")

        if vectors_to_update:
            sql = "UPDATE magazine_contents SET vector_representation = %s WHERE id = %s" # SQL query
            sql = sql + "  REFRESH MATERIALIZED VIEW CONCURRENTLY my_materialized_view;"
            execute_batch(cursor, sql, vectors_to_update) # Use execute_batch
            db.commit()
            return {"message": f"Vectors updated for {len(vectors_to_update)} records."}
        else:
            return {"message": "No valid vectors to update."}

    except psycopg2.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during vector update: {e}")
    except HTTPException as e:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred during vector update: {e}")
    finally:
        cursor.close()