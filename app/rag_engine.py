
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Load PDF
data = PyPDFLoader("data/Assignment_AI_Cyf.pdf").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
docs = splitter.split_documents(data)

# Embeddings & Vector Store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
store = InMemoryVectorStore(embeddings)
store.add_documents(docs)

# Prompt and LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
prompt = hub.pull("rlm/rag-prompt")

def query_rag(question: str) -> str:
    relevant_docs = store.similarity_search(question)
    content = "\n\n".join(doc.page_content for doc in relevant_docs)
    chat = prompt.invoke({"question": question, "context": content})
    return llm.invoke(chat).content

###############################3
import sqlite3
from langchain_core.documents import Document

# You'll need to define embeddings and store outside this function
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# store = InMemoryVectorStore(embeddings)

def load_complaints_into_vector_store(database_path="complaints.db", vector_store=None):
    """
    Reads all complaints from the SQLite database and adds them to the vector store.

    Args:
        database_path (str): The path to the SQLite database file.
        vector_store: The LangChain vector store object to add the documents to.
                      If None, it's assumed you have a global 'store' object.
    """
    if vector_store is None:
        # Assuming you have a global 'store' object initialized elsewhere
        # If not, you should pass it as an argument
        global store
        if 'store' not in globals() or not isinstance(store, InMemoryVectorStore):
            raise ValueError("Vector store is not initialized or not passed as argument.")
        target_store = store
    else:
        target_store = vector_store

    try:
        # Connect to the database
        conn = sqlite3.connect(database_path, check_same_thread=False)
        cursor = conn.cursor()

        # Select all complaints
        cursor.execute("SELECT complaint_id, name, phone_number, email, complaint_details, created_at FROM complaints")
        rows = cursor.fetchall()  # Fetch all rows from the result set

        # Create Document objects and add to the vector store
        documents = []
        for row in rows:
            complaint_id, name, phone, email, details, created_at = row
            complaint_document = Document(
                page_content=details,
                metadata={
                    "complaint_id": complaint_id,
                    "name": name,
                    "phone_number": phone,
                    "email": email,
                    "created_at": created_at
                }
            )
            documents.append(complaint_document)

        if documents:
            target_store.add_documents(documents)
            print(f"Loaded {len(documents)} complaints into the vector store.")
        else:
            print("No complaints found in the database to load.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close() # Always close the connection

# Example usage (assuming 'embeddings' and 'store' are initialized beforehand):
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import InMemoryVectorStore

# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# store = InMemoryVectorStore(embeddings)

# Load existing complaints from the database into the vector store
# load_complaints_into_vector_store("complaints.db", store)
load_complaints_into_vector_store(database_path="complaints.db", vector_store=None)
