import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

# Page config
st.set_page_config(page_title="Medical Chatbot", page_icon="🏥")

st.title("🏥 AI Medical Assistant")
st.caption("⚠️ This chatbot provides general health information only. Not a doctor.")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

SYSTEM_PROMPT = """
You are a strict medical assistant AI.

RULES:
1. ONLY answer medical questions.
2. If not medical → say:
   "❌ This assistant is only for medical-related questions."
3. No diagnosis or prescriptions.
4. Emergency → advise immediate help.
"""

# Show chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Describe your symptoms...")

if user_input:
    st.chat_message("user").markdown(user_input)

    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    # Combine prompt + history
    chat_text = SYSTEM_PROMPT + "\n\n"

    for msg in st.session_state["messages"]:
        chat_text += f"{msg['role']}: {msg['content']}\n"

    # ✅ Gemini response
    response = model.generate_content(chat_text)

    ai_reply = response.text

    with st.chat_message("assistant"):
        st.markdown(ai_reply)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": ai_reply
    })