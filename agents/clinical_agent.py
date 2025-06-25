import os
import google.generativeai as genai
from dotenv import load_dotenv
from embeddings.embed_utils import search_reference

from textblob import TextBlob

def autocorrect_query(query):
    blob = TextBlob(query)
    corrected = str(blob.correct())
    return corrected


# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.0-flash")


# 🧠 Gemini fallback response
def ask_gemini(symptom, patient):
    prompt = (
        f"A patient named {patient['patient_name']} was discharged with the condition: {patient['primary_diagnosis']}.\n"
        f"They are now experiencing the symptom: {symptom}.\n"
        "Please provide a general medical explanation of the symptom based on typical post-discharge nephrology cases.\n"
        "The tone should be informative, safe, and cautious — avoid prescriptive language or acting like a doctor."
    )
    response = model.generate_content(prompt)
    return response.text


# 🩺 Main agent logic
def clinical_response(symptom, patient):
    name = patient['patient_name']
    diagnosis = patient['primary_diagnosis']

    results = search_reference(symptom)

    # === Fallback rules ===
    threshold = 0.1             # semantic similarity cutoff
    min_chunk_length = 100       # minimum text length to count as meaningful

    if not results:
        use_fallback = True
        top_score = 0.0
        top_chunk = ""
    else:
        top_chunk, top_distance = results[0]
        top_score = 1 - top_distance
        use_fallback = (top_score < threshold) or (len(top_chunk.strip()) < min_chunk_length)

    # === Debug logs ===
    # print(f"\n[DEBUG] Query: {symptom}")
    # for i, (doc, dist) in enumerate(results):
    #     similarity = 1 - dist
    #     print(f"[{i}] Similarity: {similarity:.3f} | Chunk:\n{doc[:300]}\n---\n")
    # print(f"[DEBUG] Top similarity score: {top_score:.3f} | Fallback triggered: {use_fallback}")

    # === Gemini fallback ===
    if use_fallback:
        ai_response = ask_gemini(symptom, patient)
        return (
            f"Hi {name}, I couldn't find anything in your nephrology discharge reference about:\n\n"
            f"**\"{symptom}\"**\n\n"
            f"However, here's some general information that may help:\n\n"
            f"{ai_response}\n\n"
            "⚠️ Please remember: this is not medical advice. Always consult your doctor."
        )

    # === Book-based (RAG) response ===
    response = (
        f"Hi {name}, based on your condition (*{diagnosis}*) and your symptom:\n\n"
        f"**\"{symptom}\"**\n\n"
        f"Here's what I found from your nephrology discharge reference:\n\n"
    )

    for i, (doc, _) in enumerate(results, 1):
        response += f"🔹 *Excerpt {i}:*\n{doc}\n\n"

    response += "\n⚠️ *This information is for reference only. Always consult your physician.*"
    return response
