# neo4j_utils.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

# Load Neo4j connection details
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def get_context_from_neo4j(topic):
    with driver.session() as session:
        query = (
            "MATCH (p:Paper) WHERE p.topic = $topic "
            "RETURN p.abstract AS context LIMIT 1"
        )
        result = session.run(query, topic=topic)
        record = result.single()
        return record["context"] if record else None
