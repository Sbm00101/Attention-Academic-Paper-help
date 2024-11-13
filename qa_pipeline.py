# qa_pipeline.py
from transformers import pipeline
from neo4_utils import get_context_from_neo4j  # Import from the new utility file

# Set up the Question Answering model
qa_model = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")


def process_query(query, topic):
    # Retrieve the context from Neo4j
    context = get_context_from_neo4j(topic)

    if context:
        response = qa_model({"question": query, "context": context})
        return response['answer']
    else:
        return "No relevant context found for the given topic in Neo4j."
