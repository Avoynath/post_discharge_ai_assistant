import re

def chunk_text(text, chunk_size=500):
    # Remove blank lines and unnecessary whitespace
    cleaned_text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + " "
        else:
            if len(current.strip()) > 30:
                chunks.append(current.strip())
            current = sentence + " "

    if len(current.strip()) > 30:
        chunks.append(current.strip())

    return chunks
