import arxiv
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


def fetch_and_load_documents(topic, max_results=5):
    try:
        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        documents = []
        with driver.session() as session:
            for result in search.results():
                doc = {
                    "title": result.title,
                    "abstract": result.summary,
                    "published_date": result.published.strftime('%Y-%m-%d'),
                    "authors": [author.name for author in result.authors],
                    "pdf_url": result.pdf_url,
                    "topic": topic
                }

                session.run(
                    "MERGE (p:Paper {title: $title, abstract: $abstract, published_date: $published_date, "
                    "authors: $authors, pdf_url: $pdf_url, topic: $topic})",
                    title=doc["title"],
                    abstract=doc["abstract"],
                    published_date=doc["published_date"],
                    authors=doc["authors"],
                    pdf_url=doc["pdf_url"],
                    topic=topic
                )
                documents.append(doc)

        return documents
    except Exception as e:
        print(f"An error occurred in fetch_and_load_documents: {str(e)}")
        raise e
