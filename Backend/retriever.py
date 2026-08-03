from Backend.embeddings import model


def retrieve(query, vector_store, chunks, k=5):
    """
    Retrieve the most relevant resume chunks for a query.
    """

    # Convert query into embedding
    query_embedding = model.encode([query])[0]

    # Search the vector store
    scores, indices = vector_store.search(query_embedding, k)

    print("\nSimilarity Scores:")
    print(scores)

    # Retrieve matching chunks
    results = []

    for idx in indices[0]:
        if idx != -1:
            results.append(chunks[idx])

    return results