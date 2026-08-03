def chunk_text(text, chunk_size=350, overlap=75):
    """
    Split resume into overlapping text chunks.
    Works for any resume format.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks