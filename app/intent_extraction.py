
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an assistant for a customer complaint chatbot. 
Extract the intent and available fields from the message.

Valid intents:
- register_complaint
- check_status
- faq
- exit_faq
- greeting

Respond ONLY in this JSON format:
{{
  "intent": "...",
  "name": "...",
  "email": "...",
  "phone_number": "...",
  "complaint_details": "...",
  "complaint_id": "..."
}}

User message: {message}
""")



# prompt = ChatPromptTemplate.from_messages([
#     ("system", 
#     """You are an assistant for a customer complaint chatbot. 
# Extract the user's intent and available fields from their message. The user may provide their name, email, phone number, complaint details, or a complaint ID.
# The user enter digits equal to 10 digits for phone number.

# Valid intents:
# - register_complaint
# - check_status
# - faq
# - exit_faq
# - greeting

# Respond ONLY in this JSON format:
# {
#   "intent": "...",
#   "name": "...",
#   "email": "...",
#   "phone_number": "...",
#   "complaint_details": "...",
#   "complaint_id": "..."
# }"""),

#     # Few-shot examples
#     ("human", "I want to register a complaint"),
#     ("ai", """{
#   "intent": "register_complaint",
#   "name": "",
#   "email": "",
#   "phone_number": "4521556489",
#   "complaint_details": "",
#   "complaint_id": ""
# }"""),

#     ("human", "sunil"),
#     ("ai", """{
#   "intent": "register_complaint",
#   "name": "sunil",
#   "email": "",
#   "phone_number": "",
#   "complaint_details": "",
#   "complaint_id": ""
# }"""),

#     ("human", "my email is sunil@gmail.com"),
#     ("ai", """{
#   "intent": "register_complaint",
#   "name": "",
#   "email": "sunil@gmail.com",
#   "phone_number": "",
#   "complaint_details": "",
#   "complaint_id": ""
# }"""),

#     ("human", "status of complaint 1234"),
#     ("ai", """{
#   "intent": "check_status",
#   "name": "",
#   "email": "",
#   "phone_number": "",
#   "complaint_details": "",
#   "complaint_id": "1234"
# }"""),

#     # Final actual user input
#     ("human", "{message}")
# ])

chain = prompt | llm | parser

def extract_intent(user_input: str):
    return chain.invoke({"message": user_input})