import streamlit as st
import requests

# Set FastAPI endpoint
API_URL = "http://127.0.0.1:8050"  # Replace with your FastAPI URL if different

st.title("Academic Research Assistant")
st.write("Enter a research topic to fetch related papers, ask questions, and explore.")

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
            st.write("**Answer:**", answer_data["result"])
        else:
            st.error("Failed to get an answer. Please try again.")
    else:
        st.warning("Please enter both a topic and a question.")

# Future Work Suggestions Button (if implemented in the backend)
if st.button("Suggest Future Works"):
    if topic:
        response = requests.post(f"{API_URL}/future_works", json={"topic": topic})
        if response.status_code == 200:
            suggestion_data = response.json()
            st.write("**Future Works Suggestions:**", suggestion_data["message"])
        else:
            st.error("Failed to retrieve future works suggestions.")
    else:
        st.warning("Please enter a topic.")
