# Pre Requisites
1. Download and install Postgres version 16: https://www.postgresql.org/download/
2. Download and install PGVector in Postgres DB, https://github.com/pgvector/pgvector
3. Python version 3.12.8

# Serach APIs

This project is implemented API with two endpoint to perform a hybrid search in a table of 1 million records, 

# Below are the steps to set up the project:

## Step 1: Create below tables 

### Magazine Information (execute [Create-magazine.sql](Create-magazine.sql) in postgres)
    o Fields:
    | id | title | author | publication_date | category|

### Magazine Content (execute [Create-magazine_contents.sql](Create-magazine_contents.sql))
    o Fields:
    | id | magazine_id | content | vector_representation |
    
## Step 2: Generate data into tables 
Random data is generated and inserted in both the tables by executing insert query in [data-magazine.sql](data-magazine.sql) and [data-magazine_content.sql](data-magazine_content.sql) files.

## Step3: Create Materialize View (execute [create-magazine_search_view.sql](create-magazine_search_view.sql) in postgres)
For fast serach hnsw index on vector_representation field and gin index on text_col is added for faster search

## Step4: Install Python dependencies
    pip install -r requirements.txt  # Python (FastAPI)

## Step 5: Start the API server
    uvicorn app:main --reload  # For FastAPI    

## step 6: Open below url on browser for API doc
http://localhost:8000/docs


### API Endpoints
| Method | Endpoint        | Description          |
|--------|-----------------|----------------------|
| GET    | `/api/search`   | Fetch Data by string |
| POST   | `/api/Update`   | Create embadding of content column|  


## Step 7: Execute/api/update API
By running this API, all embadding of content field in magazine_content table will be generate using 'all-mpnet-base-v2' model
and it wll also update 'magazine_search_view' material view

## Step 8: Execute /api/search API
This API has 2 query param 'query'and 'limit', in query pass the string you want to search in data base, in limit pass the value of limit you want to see in result.

# Project Overview
This API provides a hybrid search mechanism for a magazine database containing 1 million records. It efficiently combines traditional keyword-based search with vector similarity search, ensuring highly relevant search results.


Contact
📩 Email: shreyasbhargavauk@gmail.com
🌐 GitHub: Shreyas Bhargava
