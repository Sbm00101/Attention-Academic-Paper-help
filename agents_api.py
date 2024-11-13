# agents_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from documentloader import fetch_and_load_documents
from qa_pipeline import process_query
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Neo4j driver
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

app = FastAPI()

class SearchRequest(BaseModel):
    topic: str
    max_results: Optional[int] = 5

class QueryRequest(BaseModel):
    topic: str
    query: str

@app.get("/")
async def root():
    return {"message": "Academic Research Assistant API is up and running!"}

@app.post("/search_papers")
async def search_papers(request: SearchRequest):
    try:
        documents = fetch_and_load_documents(request.topic, request.max_results)
        return {"message": f"Successfully added {len(documents)} papers to Neo4j.", "papers": documents}
    except Exception as e:
        print(f"An error occurred in /search_papers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error during paper search: {str(e)}")

@app.post("/answer_query")
async def answer_query(request: QueryRequest):
    try:
        result = process_query(request.query, request.topic)
        return {"topic": request.topic, "query": request.query, "result": result}
    except Exception as e:
        print(f"An error occurred in /answer_query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during query processing.")

@app.post("/future_works")
async def future_works(request: SearchRequest):
    try:
        return {"message": "Future works suggestions feature not implemented yet."}
    except Exception as e:
        print(f"An error occurred in /future_works: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error in future works suggestion.")

def query_by_topic_and_date(topic: str, start_year: int, end_year: int):
    try:
        with driver.session() as session:
            query = (
                "MATCH (p:Paper) "
                "WHERE p.topic = $topic AND p.published_date >= date($start_year + '-01-01') "
                "AND p.published_date <= date($end_year + '-12-31') "
                "RETURN p.title AS title, p.abstract AS abstract, p.published_date AS published_date"
            )
            result = session.run(query, topic=topic, start_year=start_year, end_year=end_year)
            papers = [{"title": record["title"], "abstract": record["abstract"], "published_date": record["published_date"]} for record in result]
            return papers
    except Exception as e:
        print(f"An error occurred in query_by_topic_and_date: {str(e)}")
        return []
