from query_parser import detect_intent, extract_entities


# Test function for detecting intents
def test_detect_intent():
    # Define a list of test queries and their expected intents
    test_cases = [
        ("Show papers on Deep learning", "search_papers"),
        ("Find future research for AI", "future_works"),
        ("Summarize recent advancements in machine learning", "qa"),
        ("Get papers on neural networks between 2019 and 2023", "database_query")
    ]

    print("Testing detect_intent function...")
    for query, expected_intent in test_cases:
        detected_intent = detect_intent(query)
        print(f"Query: '{query}' | Expected Intent: '{expected_intent}' | Detected Intent: '{detected_intent}'")
        assert detected_intent == expected_intent, f"Failed on query: {query}"


# Test function for extracting entities
def test_extract_entities():
    # Define test cases with expected outputs
    test_cases = [
        ("Show papers on Deep learning", {"topic": "Deep learning"}),
        ("Get papers on neural networks between 2019 and 2023",
         {"topic": "neural networks", "start_year": 2019, "end_year": 2023}),
        ("Find future research for AI", {"topic": "AI"}),
        ("Summarize recent advancements in machine learning", {"topic": "machine learning"})
    ]

    print("\nTesting extract_entities function...")
    for query, expected_entities in test_cases:
        entities = extract_entities(query)
        print(f"Query: '{query}' | Expected Entities: {expected_entities} | Extracted Entities: {entities}")
        assert entities == expected_entities, f"Failed on query: {query}"


# Run the tests
if __name__ == "__main__":
    test_detect_intent()
    test_extract_entities()
