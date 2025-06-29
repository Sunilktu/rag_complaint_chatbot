# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from dotenv import load_dotenv
# load_dotenv()
# from app.intent_extraction import extract_intent
# from app.rag_engine import query_rag
# import streamlit as st
# import requests

# # ====================
# # STREAMLIT UI SETUP
# # ====================
# st.title("🛠️ RAG-Based Complaint Chatbot")

# # Initialize session state
# for var in ["register_mode", "faq_mode", "details", "history","greeting_mode","check_status_mode"]:
#     if var not in st.session_state:
#         st.session_state[var] = {} if var == "details" else []

# if 'step' not in st.session_state:
#     st.session_state.step = 0

# # Handle quick-suggestion button input
# default_value = st.session_state.pop('suggested_input', "")

# REQUIRED_FIELDS = ["name", "phone_number", "email", "complaint_details"]

# # Main chat input
# prompt_input = st.chat_input("Type your message here...", key="chat_input")
# if prompt_input:
#     # Handle FAQ queries dynamically

#     st.session_state.history.append(("You", prompt_input))
#         # Complaint Registration
#     if st.session_state.register_mode and "bot_response" not in locals():
#         missing = [f for f in REQUIRED_FIELDS if f not in st.session_state.details]
#         if missing:
#             prompts = {
#                 "name": "Please provide your name.",
#                 "phone_number": "What's your phone number?",
#                 "email": "May I have your email address?",
#                 "complaint_details": "Please describe your complaint."
#             }
#             bot_response = prompts[missing[0]]
#         else:
#             response = requests.post("http://localhost:8000/complaints", json=st.session_state.details)
#             complaint_id = response.json().get("complaint_id", "N/A")
#             bot_response = f"✅ Complaint registered! Your ID is **{complaint_id}**."
#             st.session_state.register_mode = False
#             st.session_state.details = {}
            
#     elif st.session_state.faq_mode:
#         answer = query_rag(prompt_input)
#         if answer:
#             bot_response = answer
#         else:
#             bot_response = "I'm sorry, I couldn't find a relevant answer. Try rephrasing your question."
#     elif st.session_state.check_status_mode:
#         result = extract_intent(prompt_input)
#         complaint_id = result.get("complaint_id")
#         if complaint_id:
#             response = requests.get(f"http://localhost:8000/complaints/{complaint_id}")
#             if response.status_code == 200:
#                 bot_response = f"Complaint Status:\n{response.json()}"
#             else:
#                 bot_response = "Complaint not found or invalid ID."
#         else:
#             bot_response = "Please provide a valid complaint ID."
#     elif st.session_state.greeting_mode:
#         bot_response = "Hi there! How can I assist you today? You can ask questions, register complaints, or check complaint status."
#     else:
#         # Extract intent and fields from the input
      
#         result = extract_intent(prompt_input)

#         intent = result.get("intent", "").lower()

#         # Update non-empty fields
#         for field in REQUIRED_FIELDS:
#             value = result.get(field)
#             if isinstance(value, str) and value.strip():
#                 st.session_state.details[field] = value.strip()

#         # --- INTENT LOGIC ---
#         if intent == "register_complaint":
#             st.session_state.register_mode = True
#             st.session_state.faq_mode = False
#             st.session_state.greeting_mode = False
#             st.session_state.check_status_mode = False
#             st.sessiion_state.deta
#             bot_response = "You're in registration mode. Please provide your details."
#         elif intent == "check_status":
#             st.session_state.check_status_mode = True
#             st.session_state.register_mode = False
#             st.session_state.faq_mode = False
#             st.session_state.greeting_mode = False
#             bot_response = "Please provide your complaint ID to check the status."
#         elif intent == "greeting":
#             st.session_state.greeting_mode = True
#             st.session_state.register_mode = False
#             st.session_state.faq_mode = False
#             st.session_state.check_status_mode = False
#             bot_response = "Hi there! How can I assist you today? You can ask questions, register complaints, or check complaint status."
#         else:
#             st.session_state.register_mode = False
#             st.session_state.faq_mode = False
#             st.session_state.greeting_mode = False
#             st.session_state.check_status_mode = False
#             bot_response = "I'm not sure what you meant. Try asking for help or registering a complaint."
#     #     # elif intent == "register_complaint" and st.session_state.register_mode:
#     #     #     # If already in registration mode, continue collecting details
#     #     #     missing = [f for f in REQUIRED_FIELDS if f not in st.session_state.details]
#     #     #     if missing:
#     #     #         prompts = {
#     #     #             "name": "Please provide your name.",
#     #     #             "phone_number": "What's your phone number?",
#     #     #             "email": "May I have your email address?",
#     #     #             "complaint_details": "Please describe your complaint."
#     #     #         }
#     #     #         bot_response = prompts[missing[0]]
#     #     #     else:
#     #     #         response = requests.post("http://localhost:8000/complaints", json=st.session_state.details)
#     #     #         complaint_id = response.json().get("complaint_id", "N/A")
#     #     #         bot_response = f"✅ Complaint registered! Your ID is **{complaint_id}**."
#     #     #         st.session_state.register_mode = False
#     #     #         st.session_state.details = {}
#     #     # elif intent == "faq" and not st.session_state.faq_mode: 

#     # elif intent in ["faq", "help"]:
#     #     st.session_state.faq_mode = True
#     #     st.session_state.register_mode = False
#     #     bot_response = "You're in FAQ mode. Ask your question."

#     # # # If in FAQ mode, always query RAG regardless of detected intent
#     # # elif st.session_state.faq_mode:
#     # #     answer = query_rag(prompt_input)
#     # #     bot_response = answer if answer else "I'm sorry, I couldn't find a relevant answer. Try rephrasing your question."


#     # elif intent in ["exit", "back", "exit_faq"]:
#     #     st.session_state.faq_mode = False
#     #     st.session_state.register_mode = False
#     #     bot_response = "Exited current mode."
#     #     # Clear details only if not in registration mode
#     #     if not st.session_state.register_mode:
#     #         st.session_state.details = {}


#     # elif (intent == "check_status" or result.get("complaint_id")) and not (st.session_state.register_mode or st.session_state.faq_mode):
#     #     st.session_state.faq_mode = False
#     #     st.session_state.register_mode = False
#     #     # Only clear details if not in register mode
#     #     if not st.session_state.register_mode:
#     #         st.session_state.details = {}

#     #     cid = result.get("complaint_id")
#     #     if cid:
#     #         response = requests.get(f"http://localhost:8000/complaints/{cid}")
#     #         bot_response = f"Complaint Status:\n{response.json()}" if response.status_code == 200 else "Complaint not found or invalid ID."
#     #     else:
#     #         bot_response = "Please provide a valid complaint ID."
#     # # If in FAQ mode, always query RAG regardless of detected intent

            



#     # elif intent == "greeting":
#     #     bot_response = "Hi there! How can I assist you today? You can ask questions register complaints and retrive complaints."

#     # elif "bot_response" not in locals():
#     #     bot_response = "I'm not sure what you meant. Try asking for help or registering a complaint."

#     # st.session_state.history.append(("Bot", bot_response))

# # Show Chat History
# st.subheader("Chat History")
# for speaker, msg in st.session_state.history:
#     st.markdown(f"**{speaker}:** {msg}")

# # Quick Buttons
# st.markdown("---")
# st.markdown("### 💡 Quick Suggestions")
# col1, col2, col3 = st.columns(3)
# with col1:
#     if st.button("Help / FAQ"):
#         st.session_state.suggested_input = "help"
# with col2:
#     if st.button("Register Complaint"):
#         st.session_state.suggested_input = "register complaint"
# with col3:
#     if st.button("Check Complaint Status"):
#         st.session_state.suggested_input = "status of complaint ABC123"


# # import sys
# # import os
# # import streamlit as st
# # import requests
# # from dotenv import load_dotenv

# # # Importing from parent directory
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# # load_dotenv()

# # from app.intent_extraction import extract_intent
# # from app.rag_engine import query_rag

# # # ====================
# # # STREAMLIT UI SETUP
# # # ====================
# # st.title("🛠️ RAG-Based Complaint Chatbot")

# # REQUIRED_FIELDS = ["name", "phone_number", "email", "complaint_details"]

# # # Initialize session state
# # if 'history' not in st.session_state:
# #     st.session_state.history = []

# # if 'details' not in st.session_state:
# #     st.session_state.details = {}

# # if 'mode' not in st.session_state:
# #     st.session_state.mode = None  # can be 'faq', 'register', or None


# # # Main chat input
# # prompt_input = st.chat_input("Type your message here...")

# # # ================
# # # HANDLE RESPONSE
# # # ================
# # def handle_faq_mode(query):
# #     answer = query_rag(query)
# #     return answer if answer else "I'm sorry, I couldn't find a relevant answer. Try rephrasing your question."

# # def handle_register_mode(result):
# #     # Update only non-empty fields
# #     for field in REQUIRED_FIELDS:
# #         value = result.get(field)
# #         if value and isinstance(value, str) and value.strip():
# #             st.session_state.details[field] = value.strip()
    
# #     # Check if all fields are filled
# #     missing_fields = [f for f in REQUIRED_FIELDS if f not in st.session_state.details]
# #     if missing_fields:
# #         prompts = {
# #             "name": "Please provide your name.",
# #             "phone_number": "What's your phone number?",
# #             "email": "May I have your email address?",
# #             "complaint_details": "Please describe your complaint."
# #         }
# #         return prompts[missing_fields[0]]
# #     else:
# #         response = requests.post("http://localhost:8000/complaints", json=st.session_state.details)
# #         complaint_id = response.json().get("complaint_id", "N/A")
# #         st.session_state.details = {}
# #         st.session_state.mode = None
# #         return f"✅ Complaint registered! Your ID is **{complaint_id}**."


# # if prompt_input:
# #     st.session_state.history.append(("You", prompt_input))
# #     result = extract_intent(prompt_input)
# #     intent = result.get("intent", "").lower()

# #     # --- Exit Mode ---
# #     if intent in ["exit", "back", "exit_faq"]:
# #         st.session_state.mode = None
# #         st.session_state.details = {}
# #         bot_response = "Exited current mode."

# #     # --- Greeting ---
# #     elif intent == "greeting":
# #         bot_response = "Hi there! How can I assist you today? You can ask questions, register complaints, or check complaint status."

# #     # --- FAQ Mode ---
# #     elif intent in ["faq", "help"]:
# #         st.session_state.mode = "faq"
# #         bot_response = "You're now in FAQ mode. Ask your question."

# #     elif st.session_state.mode == "faq":
# #         bot_response = handle_faq_mode(prompt_input)

# #     # --- Complaint Status ---
# #     elif intent == "check_status" or result.get("complaint_id"):
# #         cid = result.get("complaint_id")
# #         if cid:
# #             response = requests.get(f"http://localhost:8000/complaints/{cid}")
# #             if response.status_code == 200:
# #                 bot_response = f"Complaint Status:\n{response.json()}"
# #             else:
# #                 bot_response = "Complaint not found or invalid ID."
# #         else:
# #             bot_response = "Please provide a valid complaint ID."

# #     # --- Register Complaint ---
# #     elif intent == "register_complaint":
# #         st.session_state.mode = "register"
# #         bot_response = handle_register_mode(result)

# #     elif st.session_state.mode == "register":
# #         bot_response = handle_register_mode(result)
    
# #     elif intent == "greeting" and not st.session_state.mode== "register":
# #         bot_response = "Hi there! How can I assist you today? You can ask questions, register complaints, or check complaint status."
# #     # --- Unknown Intent ---
# #     else:
# #         bot_response = "I'm not sure what you meant. Try asking for help or registering a complaint."

# #     st.session_state.history.append(("Bot", bot_response))

# # # ==================
# # # DISPLAY CHAT
# # # ==================
# # st.subheader("Chat History")
# # for speaker, msg in st.session_state.history:
# #     st.markdown(f"**{speaker}:** {msg}")

# # # ==================
# # # QUICK SUGGESTIONS
# # # ==================
# # st.markdown("---")
# # st.markdown("### 💡 Quick Suggestions")
# # col1, col2, col3 = st.columns(3)
# # with col1:
# #     if st.button("Help / FAQ"):
# #         st.session_state.history.append(("You", "help"))
# #         st.rerun()
# # with col2:
# #     if st.button("Register Complaint"):
# #         st.session_state.history.append(("You", "register complaint"))
# #         st.rerun()
# # with col3:
# #     if st.button("Check Complaint Status"):
# #         st.session_state.history.append(("You", "status of complaint ABC123"))
# #         st.rerun()


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
