# Serach APIs

This project is implemented API with two endpoint to perform a hybrid search in a table of 1 million records, 
• Table 1: Magazine Information
    o Fields: id, title, author, publication_date, category, etc.
• Table 2: Magazine Content
    o Fields: id, magazine_id (foreign key to Magazine Information), content, vector_representation, etc.
Random data is generated and inserted in both the tables via insert script, magazine.sql and magazine_content.sql



## Below are the steps to set up the application :

1. 


# Project Overview
This API provides a hybrid search mechanism for a magazine database containing 1 million records. It efficiently combines traditional keyword-based search with vector similarity search, ensuring highly relevant search results.

## Features
✅ Hybrid Search: Combines keyword and vector-based search for enhanced accuracy.
✅ Scalability: Optimized to handle 1 million records efficiently.
✅ Full-Text Search: Enables fast searches in magazine titles, authors, and content.
✅ Vector Search: Uses embeddings to find semantically similar content.
✅ Indexing & Performance: Utilizes indexing techniques for fast retrieval.

## API Endpoints
| Method | Endpoint        | Description          |
|--------|-----------------|----------------------|
| GET    | `/api/search`   | Fetch Data by string |
| POST   | `/api/Update`   | Create embadding of content column|



## Database Schema
📚 Table 1: Magazine Information
Stores general magazine details.

|Column Name | Type |	Description |
|id	INT (PK) |	Unique |  magazine identifier |
|title	| TEXT	| Title of the magazine |
|author	| TEXT |	Author of the magazine|
|publication_date|	DATE |	Date of publication|
|category|	TEXT |	Category of the magazine |


📝 Table 2: Magazine Content
Stores magazine content along with vector embeddings for semantic search.

|Column Name |	Type |	Description |
| id	INT (PK) |	Unique | content identifier |
| magazine_id	INT (FK) |	Reference to Magazine Information |
| content |	TEXT	|Full text content of the magazine |
| vector_representation |	VECTOR| 	Embedding representation for search|


## Search Functionality
1️⃣ Keyword-Based Search
Searches in title, author, and content fields.
Uses PostgreSQL Full-Text Search (to_tsvector, phraseto_tsquery, ts_rank) for efficiency.
2️⃣ Vector Search
Uses vector similarity search to find semantically relevant content.
Requires PGVector or another vector search solution in PostgreSQL.
3️⃣ Hybrid Search
Combines both keyword and vector search results.

# Install dependencies
pip install -r requirements.txt  # Python (FastAPI)

# Start the API
uvicorn app:main --reload  # For FastAPI

Contact
📩 Email: shreyasbhargavauk@gmail.com
🌐 GitHub: Shreyas Bhargava
