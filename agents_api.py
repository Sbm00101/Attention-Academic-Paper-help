from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from documentloader import fetch_and_load_documents
from qa_pipeline import process_query
from neo4_utils import get_context_from_neo4j  # Ensure we have this utility file set up
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
        suggestions = suggest_future_works(request.topic)
        return {"topic": request.topic, "future_works": suggestions}
    except Exception as e:
        print(f"An error occurred in /future_works: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error in future works suggestion.")


# Helper function to suggest future works based on the topic
def suggest_future_works(topic: str):
    suggestions = []
    try:
        with driver.session() as session:
            # Query to get recent research abstracts for the given topic
            query = (
                "MATCH (p:Paper) WHERE p.topic = $topic "
                "RETURN p.abstract AS abstract LIMIT 5"
            )
            results = session.run(query, topic=topic)
            abstracts = [record["abstract"] for record in results]

            # Basic heuristic to suggest future work (more sophisticated NLP can be added)
            if abstracts:
                suggestions.append("Explore applications of new findings in practical settings.")
                suggestions.append("Conduct longitudinal studies to observe the long-term effects.")
                suggestions.append("Investigate unresolved questions noted in recent studies.")
                suggestions.append("Examine limitations mentioned in related studies for future improvements.")
            else:
                suggestions.append(
                    "No existing research found in the database. Consider starting foundational studies.")

    except Exception as e:
        print(f"An error occurred in suggest_future_works: {str(e)}")

    return suggestions
