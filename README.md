# 🩺 Post-Discharge Medical AI Assistant

A modular AI-powered assistant for post-discharge patient support, leveraging retrieval-augmented generation (RAG) and LLMs to answer patient questions, provide follow-up guidance, and reference clinical materials.

---

## 🚀 Features

- **Patient Lookup**: Search and display patient discharge summaries from structured data.
- **Reference-Aware Q&A**: Answers patient questions using a vector database of clinical reference material (e.g., nephrology PDF).
- **LLM Fallback**: Uses Gemini LLM for general medical explanations if no relevant reference is found.
- **Follow-Up Guidance**: Receptionist agent suggests follow-up questions and reminders.
- **Chat Logging**: All interactions are logged for review and debugging.
- **Extensible**: Modular agents and tools for easy adaptation to other specialties or data sources.

---

## 🗂️ Directory Structure

```
post_discharge_ai_assistant/
  agents/           # AI agent logic (clinical, receptionist)
  data/             # Patient data and reference PDFs
  embeddings/       # Embedding utilities and persistent ChromaDB vector store
  frontend/         # Streamlit app for user interaction
  scripts/          # Utilities for indexing and debugging
  tools/            # PDF loader, text splitter, database helpers
  requirements.txt  # Python dependencies
  README.md         # Project documentation
```

---

## ⚡ Quickstart

### 1. **Clone & Install**
```bash
pip install -r requirements.txt
```

### 2. **Prepare API Keys**
Create a `.env` file in the project root with your Gemini API key:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. **Index Reference Material**
By default, the project uses `data/nephrology.pdf` as the reference. To (re)index:
```bash
python scripts/index_reference.py
```
This will extract, chunk, embed, and store the PDF in `embeddings/chromadb`.

### 4. **Run the Frontend**
```bash
python -m streamlit run frontend/app.py
```
Open the provided URL in your browser to interact with the assistant.

---

## 🏥 Usage

- **Patient Search**: Enter your name to retrieve your discharge summary.
- **Follow-Up Guidance**: Review suggested questions and reminders.
- **Clinical Q&A**: Chat with the clinical assistant about symptoms or post-discharge concerns. The assistant will:
  - Search the indexed reference for relevant information.
  - If nothing relevant is found, provide a general answer using Gemini LLM.
- **Logs**: All chats are saved in `chat_log.txt`.

---

## 📊 Data Format

### Patient Data (`data/dummy_patient_data.json`)
Each patient record includes:
```json
{
  "patient_name": "John Smith",
  "discharge_date": "2025-06-11",
  "primary_diagnosis": "Chronic Kidney Disease Stage 3",
  "medications": ["Hydrochlorothiazide 25mg", "Amlodipine 5mg"],
  "dietary_restrictions": "Low sodium (2g/day), fluid restriction (1.5L/day)",
  "follow_up": "Nephrology clinic in 1 week",
  "warning_signs": "Swelling, shortness of breath, decreased urine output",
  "discharge_instructions": "Stay hydrated, monitor urine output"
}
```

### Reference Material
- Place your clinical reference PDF in `data/` and update the path in `scripts/index_reference.py` if needed.

---

## 🛠️ Developer Utilities

- **Index Reference**: `python scripts/index_reference.py` (extracts, chunks, and embeds a PDF)
- **Debug Vector Store**: `python scripts/debug_vector_store.py` (test semantic search queries)
- **Clear Chat Log**: Use the button in the Streamlit UI or manually clear `chat_log.txt`.

---

## 🧩 Extending the Project

- **Add New Agents**: Implement new agent logic in `agents/` and integrate with the frontend.
- **Change Reference Material**: Replace the PDF in `data/` and re-run the indexing script.
- **Integrate More Data**: Add new fields to the patient JSON and update the UI as needed.
- **Switch LLMs**: Update the agent logic to use a different LLM or API.

---

## 📦 Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies (Streamlit, ChromaDB, sentence-transformers, PyPDF2, etc.)
- Gemini API key (for fallback LLM responses)

---

## ⚠️ Disclaimer

This assistant is for educational and demonstration purposes only. It does **not** provide medical advice. Always consult a qualified healthcare provider for medical concerns.

---
