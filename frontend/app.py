import streamlit as st
import datetime
from tools.database_tool import load_patient_data, find_patient_by_name
from agents.receptionist_agent import generate_followup_questions
from agents.clinical_agent import clinical_response, autocorrect_query

# ✅ Logging function
def log_chat(user_input, ai_output, patient_name):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Patient: {patient_name}\n")
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {ai_output}\n")
        f.write("-----\n")

# ✅ UI title
st.title("🩺 Post-Discharge Medical AI Assistant")

# Patient search input
name = st.text_input("What is your name?")

# Patient lookup and info display
if name:
    patient_data = load_patient_data()
    patient, error = find_patient_by_name(name, patient_data)

    if error:
        st.error(error)
    else:
        st.success("Patient found!")
        st.session_state.patient = patient

        # Discharge summary
        st.write(f"👤 **Name**: {patient['patient_name']}")
        st.write(f"🗓️ **Discharge Date**: {patient['discharge_date']}")
        st.write(f"🩺 **Diagnosis**: {patient['primary_diagnosis']}")
        st.write(f"💊 **Medications**: {', '.join(patient['medications'])}")
        st.write(f"🥗 **Diet**: {patient['dietary_restrictions']}")
        st.write(f"📅 **Follow-up**: {patient['follow_up']}")
        st.write(f"⚠️ **Warning Signs**: {patient['warning_signs']}")
        st.write(f"📋 **Instructions**: {patient['discharge_instructions']}")

        # Follow-up suggestions
        st.markdown("---")
        st.markdown(generate_followup_questions(patient))

        # === Chat section ===
        st.markdown("### 🤖 Chat with the Clinical Assistant")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Show chat history
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).markdown(msg["content"])

        # New symptom input
        if prompt := st.chat_input("Describe your symptom or post-discharge question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Thinking..."):
                corrected = autocorrect_query(prompt)
                response = clinical_response(corrected, patient)

            # Show and store response
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").markdown(response)

            # ✅ Log interaction
            log_chat(prompt, response, patient["patient_name"])

# Disclaimer
st.markdown("---")
st.info("⚠️ This assistant is for educational purposes only. It does not provide medical advice. Always consult your doctor.")


# Clear logs button (admin/dev use)
if st.button("🗑️ Clear Chat Log"):
    open("chat_log.txt", "w").close()
    st.success("Chat log cleared!")
