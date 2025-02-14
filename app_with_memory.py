import os
import time
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import requests

load_dotenv()

MODEL_ID = os.environ['MODEL_ID']
PDF_DIRECTORY = "./data2"  # Directory with multiple PDFs
INDEX_PATH = "./faiss_index"  # Path to save/load FAISS index
OLLAMA_URL = "http://127.0.0.1:11434"  # Connect to local Ollama server

# Initialize embeddings if not in session state
if "embeddings" not in globals():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
else:
    embeddings = globals()['embeddings']

# Function to check Ollama server connection
def check_ollama_server(url):
    try:
        # Send a GET request to the base URL (not /status)
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

# Check Ollama server connection
server_connected = check_ollama_server(OLLAMA_URL)
if server_connected:
    print(f"Ollama server connected at {OLLAMA_URL}")
else:
    print(f"Failed to connect to Ollama server at {OLLAMA_URL}")

# Initialize documents and vector store
if "vector" not in globals():
    progress_text = "Initializing..."

    # Load or create FAISS index
    if os.path.exists(INDEX_PATH):
        print("Loading FAISS index...")
        vector = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

        # Display total number of indexed documents
        total_documents = vector.index.ntotal
        print(f"Total number of indexed documents: {total_documents}")

        # If documents aren't loaded, re-fetch from PDFs and split
        if "documents" not in globals():
            all_docs = []
            pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.endswith(".pdf")]
            for filename in pdf_files:
                file_path = os.path.join(PDF_DIRECTORY, filename)
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                for doc in docs:
                    doc.metadata["source"] = os.path.basename(file_path)
                all_docs.extend(docs)
            
            # Split documents into chunks and store
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = text_splitter.split_documents(all_docs)

    else:
        # Create FAISS index from scratch
        all_docs = []
        pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.endswith(".pdf")]
        for i, filename in enumerate(pdf_files):
            file_path = os.path.join(PDF_DIRECTORY, filename)
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
            all_docs.extend(docs)

            # Update progress
            print(f"Processing {filename} ({i + 1}/{len(pdf_files)})...")

        # Split documents and create FAISS index
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.split_documents(all_docs)
        vector = FAISS.from_documents(documents, embeddings)
        vector.save_local(INDEX_PATH)
        print("FAISS index created and saved successfully.")

        # Display total number of indexed documents after creation
        total_documents = vector.index.ntotal
        print(f"Total number of indexed documents: {total_documents}")

    print("Initialization complete.")

# Terminal-based document print with index
def print_all_indexed_documents(documents):
    print("Indexed Documents:")
    for i, doc in enumerate(documents):
        filename = os.path.basename(doc.metadata.get("source", "Unknown"))
        page_number = doc.metadata.get("page", "Unknown")
        
        # Print document details
        print(f"Document {i + 1} (Index: {i}): {filename} | Page Number: {page_number}")
        print(doc.page_content)
        print("--------------------------------")

# Print all indexed documents with their original index
# print_all_indexed_documents(documents)

# Set up the app interface for prompt-based question and answer
llm = ChatGroq(
    groq_api_key=MODEL_ID, 
    model_name='llama3-70b-8192'
)

# Define the prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context. 
Think step by step before providing a detailed answer. 
I will tip you $200 if the user finds the answer helpful. 
<context>
{context}
</context>

Question: {input}""")

# Create a chain for processing the documents and query
document_chain = create_stuff_documents_chain(llm, prompt)

# Set up the retriever and retrieval chain
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Allow user input for questions
while True:
    prompt_input = input("Input your prompt here (or type 'exit' to quit): ").strip()
    if prompt_input.lower() == 'exit':
        break

    print(f"Processing prompt: {prompt_input}...")

    # Time the response for performance
    start = time.process_time()
    response = retrieval_chain.invoke({"input": prompt_input})
    print(f"Response time: {time.process_time() - start}")
    answer = response["answer"]
    print(f"Answer: {answer}")

    # Optionally display document context for the answer
    print("\nDocument Similarity Search Results:----------------------------------------------------------------")
    for i, doc in enumerate(response["context"]):
        filename = os.path.basename(doc.metadata.get("source", "Unknown"))
        page_number = doc.metadata.get("page", "Unknown")
        
        # Print document details with the original index
        original_index = next((idx for idx, d in enumerate(documents) if d.page_content == doc.page_content), "Unknown")
        print(f"Document {original_index} : {filename} | Page Number: {page_number}")
        print(doc.page_content)
        print("--------------------------------")