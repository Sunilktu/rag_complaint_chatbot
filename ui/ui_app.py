import sys
import os
import streamlit as st
import requests
from dotenv import load_dotenv
# # Get the absolute path to the parent directory (your project root)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# # Add the parent directory to sys.path
sys.path.append(parent_dir)
load_dotenv()

from app.intent_extraction import extract_intent
from app.rag_engine import query_rag
# ====================
# STREAMLIT UI SETUP
# ====================
st.title("🛠️ RAG-Based Complaint Chatbot")

REQUIRED_FIELDS = ["name", "phone_number", "email", "complaint_details"]

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'details' not in st.session_state:
    st.session_state.details = {}

if 'register_mode' not in st.session_state:
    st.session_state.register_mode = False

if 'faq_mode' not in st.session_state:
    st.session_state.faq_mode = False

if 'check_status_mode' not in st.session_state:
    st.session_state.check_status_mode = False

# Main chat input
prompt_input = st.chat_input("Type your message here...")

# ================
# CHATBOT LOGIC
# ================
if prompt_input:
    
    st.session_state.history.append(("You", prompt_input))
    bot_response = None
    # Exit logic – runs early to break out of modes
    exit_commands = ["exit", "back", "exit faq", "quit", "close"]
    if prompt_input.strip().lower() in exit_commands:
        st.session_state.register_mode = False
        st.session_state.faq_mode = False
        st.session_state.check_status_mode = False
        st.session_state.details = {}
        bot_response = "✅ Exited current mode."
        st.session_state.history.append(("Bot", bot_response))
        st.stop()  # Stops further processing for this input
    # ========== 1. Register Mode ==========
    # if st.session_state.register_mode:
    #     result = extract_intent(prompt_input)
    #     for field in REQUIRED_FIELDS:
    #         value = result.get(field)
    #         if value and isinstance(value, str):
    #             st.session_state.details[field] = value.strip()

    #     missing = [f for f in REQUIRED_FIELDS if f not in st.session_state.details]
    #     if missing:
    #         prompts = {
    #             "name": "Please provide your name.",
    #             "phone_number": "What's your phone number?",
    #             "email": "May I have your email address?",
    #             "complaint_details": "Please describe your complaint."
    #         }
    #         bot_response = prompts[missing[0]]
    #     else:
    #         response = requests.post("http://localhost:8000/complaints", json=st.session_state.details)
    #         complaint_id = response.json().get("complaint_id", "N/A")
    #         bot_response = f"✅ Complaint registered! Your ID is **{complaint_id}**."
    #         st.session_state.register_mode = False
    #         st.session_state.details = {}
    if st.session_state.register_mode:
        result = extract_intent(prompt_input)
        prompts = {
            "name": "Please provide your name.",
            "phone_number": "What's your phone number?",
            "email": "May I have your email address?",
            "complaint_details": "Please describe your complaint."}
        # Track missing fields
        missing = [f for f in REQUIRED_FIELDS if f not in st.session_state.details or not st.session_state.details[f].strip()]
        current_field = missing[0] if missing else None

        # 1. Try to extract from intent
        if current_field:
            extracted_value = result.get(current_field)
            if extracted_value and isinstance(extracted_value, str) and extracted_value.strip():
                st.session_state.details[current_field] = extracted_value.strip()
            else:
                # 2. If intent missed it, use raw input as fallback
                st.session_state.details[current_field] = prompt_input.strip()

        # 3. Recalculate missing
        missing = [f for f in REQUIRED_FIELDS if f not in st.session_state.details or not st.session_state.details[f].strip()]
        if missing:
            bot_response = prompts[missing[0]]
        else:
            # All details collected, register the complaint
            response = requests.post("http://localhost:8000/complaints", json=st.session_state.details)
            complaint_id = response.json().get("complaint_id", "N/A")
            bot_response = f"✅ Complaint registered! Your ID is **{complaint_id}**."
            st.session_state.register_mode = False
            st.session_state.details = {}

    # ========== 2. FAQ Mode ==========
    elif st.session_state.faq_mode:
        answer = query_rag(prompt_input)
        bot_response = answer if answer else "I'm sorry, I couldn't find a relevant answer. Try rephrasing your question."

    # ========== 3. Check Status Mode ==========
    elif st.session_state.check_status_mode:
        result = extract_intent(prompt_input)
        complaint_id = result.get("complaint_id")
        if complaint_id:
            response = requests.get(f"http://localhost:8000/complaints/{complaint_id}")
            if response.status_code == 200:
                bot_response = f"Complaint Status:\n{response.json()}"
            else:
                bot_response = "Complaint not found or invalid ID."
            st.session_state.check_status_mode = False
        else:
            bot_response = "Please provide a valid complaint ID."

    # ========== 4. New Intent Detection ==========
    else:
        result = extract_intent(prompt_input)
        intent = result.get("intent", "").lower()

        for field in REQUIRED_FIELDS:
            value = result.get(field)
            if value and isinstance(value, str):
                st.session_state.details[field] = value.strip()

        if intent == "register_complaint":
            st.session_state.register_mode = True
            st.session_state.faq_mode = False
            st.session_state.check_status_mode = False
            bot_response = "You're in registration mode. Please provide your name."

        elif intent == "faq":
            st.session_state.faq_mode = True
            st.session_state.register_mode = False
            st.session_state.check_status_mode = False
            bot_response = "You're in FAQ mode. Ask your question."

        elif intent == "check_status":
            st.session_state.check_status_mode = True
            st.session_state.register_mode = False
            st.session_state.faq_mode = False
            bot_response = "Please provide your complaint ID."

        elif intent == "greeting":
            bot_response = "Hi there! How can I assist you today? You can ask questions, register complaints, or check complaint status."

        elif intent in ["exit", "back", "exit_faq"]:
            st.session_state.register_mode = False
            st.session_state.faq_mode = False
            st.session_state.check_status_mode = False
            st.session_state.details = {}
            bot_response = "Exited current mode."

        else:
            bot_response = "I'm not sure what you meant. Try asking for help or registering a complaint."

    # Append bot message
    st.session_state.history.append(("Bot", bot_response))


# ==================
# DISPLAY CHAT HISTORY
# ==================
st.subheader("Chat History")
for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}")

# ==================
# QUICK SUGGESTIONS
# ==================
# st.markdown("---")
# st.markdown("### 💡 Quick Suggestions")
# col1, col2, col3 = st.columns(3)
# with col1:
#     if st.button("Help / FAQ"):
#         st.session_state.history.append(("You", "help"))
#         st.rerun()
# with col2:
#     if st.button("Register Complaint"):
#         st.session_state.history.append(("You", "register a complaint"))
#         st.rerun()
# with col3:
#     if st.button("Check Complaint Status"):
#         st.session_state.history.append(("You", "Check the complaint status"))
#         st.rerun()
