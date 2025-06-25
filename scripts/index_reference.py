import sys
import os

# 👇 Add the parent directory to sys.path so Python can find 'tools' and 'embeddings'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.pdf_loader import load_pdf_text
from tools.text_splitter import chunk_text
from embeddings.embed_utils import create_and_store_embeddings


# 📘 Load and process the PDF
pdf_path = "data/nephrology.pdf"
print(f"🔍 Loading text from: {pdf_path}")
text = load_pdf_text(pdf_path)

# ✂️ Chunk the text
print("📄 Splitting text into chunks...")
chunks = chunk_text(text)

# 🔗 Create embeddings and store them in ChromaDB
print(f"🔁 Embedding and storing {len(chunks)} chunks...")
create_and_store_embeddings(chunks)

print("✅ Done indexing the reference book.")
