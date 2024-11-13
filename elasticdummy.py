import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from .env
ELASTICSEARCH_CLOUD_ID = os.getenv("ELASTICSEARCH_CLOUD_ID")
ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")

# Initialize Elasticsearch client with Cloud ID and API key
es = Elasticsearch(
    cloud_id=ELASTICSEARCH_CLOUD_ID,
    api_key=ELASTICSEARCH_API_KEY
)
