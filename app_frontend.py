import streamlit as st
import requests

# Set FastAPI endpoint
API_URL = "http://127.0.0.1:8090"  # Update this if your FastAPI app is hosted elsewhere

st.title("Academic Research Assistant")
st.write("Enter a research topic to fetch related papers, ask questions, and explore suggestions for future research.")

# Topic input for searching papers
topic = st.text_input("Enter a research topic:")

# Search for Papers Button
if st.button("Search Papers"):
    if topic:
        response = requests.post(f"{API_URL}/search_papers", json={"topic": topic})
        if response.status_code == 200:
            data = response.json()
            st.write(f"Found {len(data['papers'])} papers on '{topic}':")
            for paper in data['papers']:
                st.write(f"**Title:** {paper['title']}")
                st.write(f"**Abstract:** {paper['abstract']}")
                st.write(f"**Published Date:** {paper['published_date']}")
                st.write(f"**Authors:** {', '.join(paper['authors'])}")
                st.write("---")
        else:
            st.error("Failed to fetch papers. Please try again.")
    else:
        st.warning("Please enter a topic.")

# Input for question-answering
query = st.text_input("Ask a question about the research topic:")

# Get Answer Button
if st.button("Get Answer"):
    if topic and query:
        response = requests.post(f"{API_URL}/answer_query", json={"topic": topic, "query": query})
        if response.status_code == 200:
            answer_data = response.json()
            if answer_data["result"] != "No relevant context found for the given topic in Neo4j.":
                st.write("**Answer:**", answer_data["result"])
            else:
                st.warning("No relevant context found for the given topic in Neo4j. Please try a different question or topic.")
        else:
            st.error("Failed to get an answer. Please try again.")
    else:
        st.warning("Please enter both a topic and a question.")

# Future Work Suggestions Button
if st.button("Suggest Future Works"):
    if topic:
        response = requests.post(f"{API_URL}/future_works", json={"topic": topic})
        if response.status_code == 200:
            suggestion_data = response.json()
            st.write("**Future Works Suggestions:**")
            for suggestion in suggestion_data["future_works"]:
                st.write(f"- {suggestion}")
        else:
            st.error("Failed to retrieve future works suggestions.")
    else:
        st.warning("Please enter a topic.")
