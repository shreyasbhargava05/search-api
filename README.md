# Pre Requisites
1. Download and install Postgres version 16: https://www.postgresql.org/download/
2. Download and install PGVector in Postgres DB, https://github.com/pgvector/pgvector
3. Python version 3.12.8

# Serach APIs

This project is implemented API with two endpoint to perform a hybrid search in a table of 1 million records, 

# Follow below steps to set up the project:

## Step 1: Create below tables 

### Magazine Information (execute [text](Create-magazine.sql) in postgres)
    o Fields: id, title, author, publication_date, category.

    | id | title        | author          | publication_date | category|
    |----|--------------|-----------------|------------------|---------|


### Magazine Content (execute [text](Create-magazine_content.sql))
    o Fields: id, magazine_id (foreign key to Magazine Information), content, vector_representation.

    | id | magazine_id        | content          | vector_representation |
    |----|--------------------|------------------|-----------------------|

## Step 2: Generate data into tables 
Random data is generated and inserted in both the tables by executing insert query in data-magazine.sql and data-magazine_content.sql files.

## Step3: Create Materialize View (execute [text](create-magazine_search_view.sql) in postgres)

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


## Step 7: Execute Update API
By running this API, all embadding of content field in magazine_content table will be generate using 'all-mpnet-base-v2' model
and it wll also update 'magazine_search_view' material view

## Step 8: Execute Search API
This API has 2 query param 'query'and 'limit', in query pass the string you want to search in data base, in limit pass the value of limit you want to see in result.

# Project Overview
This API provides a hybrid search mechanism for a magazine database containing 1 million records. It efficiently combines traditional keyword-based search with vector similarity search, ensuring highly relevant search results.


Contact
📩 Email: shreyasbhargavauk@gmail.com
🌐 GitHub: Shreyas Bhargava