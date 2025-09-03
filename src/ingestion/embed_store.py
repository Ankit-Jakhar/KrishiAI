import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever, Document
from langchain_huggingface.chat_models import ChatHuggingFace
from transformers import pipeline

# -------------------------------
# CONFIG
# -------------------------------
DATA_DIR = "F:/KrishiAI/Data"         # your PDF folder
CHROMA_DIR = "F:/KrishiAI/db/chroma"  # where embeddings will be saved

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL_NAME = "google/flan-t5-base"

QUERY_TYPES = {
    "1": "Disease",
    "2": "Organic Solution",
    "3": "Inorganic Solution",
    "4": "Crop Season",
    "5": "Temperature/Growth Conditions"
}

# -------------------------------
# LOAD AND SPLIT PDF DOCUMENTS
# -------------------------------
def load_documents():
    docs = []
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(DATA_DIR, file_name)
            loader = PyPDFLoader(file_path)
            loaded_docs = loader.load()
            docs.extend(loaded_docs)
            print(f"[INFO] Loaded {file_name} with {len(loaded_docs)} pages")
    return docs

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    print(f"[INFO] Split into {len(split_docs)} chunks")
    return split_docs

# -------------------------------
# CREATE CHROMA VECTORSTORE
# -------------------------------
def create_chroma_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    vectordb.add_documents(documents)
    vectordb.persist()
    print(f"[INFO] Stored {len(documents)} embeddings in ChromaDB")

# -------------------------------
# CUSTOM ICAR PLACEHOLDER RETRIEVER
# -------------------------------
class ICARWebRetriever(BaseRetriever):
    def get_relevant_documents(self, query: str):
        return [
            Document(
                page_content=f"ICAR placeholder for query: {query}",
                metadata={"source": "ICAR"}
            )
        ]

# -------------------------------
# HYBRID RETRIEVER (PDF + ICAR)
# -------------------------------
def create_hybrid_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    pdf_retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k":3})
    icar_retriever = ICARWebRetriever()

    def hybrid(query):
        pdf_docs = pdf_retriever.get_relevant_documents(query)
        icar_docs = icar_retriever.get_relevant_documents(query)
        return pdf_docs + icar_docs

    return hybrid

# -------------------------------
# PROMPT TEMPLATE
# -------------------------------
prompt_template = """
You are an agriculture expert assistant.
Answer the farmer query based on retrieved documents.
Query Type: {query_type}
Question: {question}
Documents:
{context}
Provide a clear, actionable answer in the language of the question (Hindi/English).
Also include the source of information for each point.
"""

PROMPT = PromptTemplate(
    input_variables=["query_type", "question", "context"],
    template=prompt_template
)

# -------------------------------
# CREATE LLM PIPELINE
# -------------------------------
def create_pipeline_chain():
    retriever = create_hybrid_retriever()

    # Initialize Hugging Face pipeline
    hf_pipe = pipeline(
        task="text2text-generation",
        model=LLM_MODEL_NAME,
        tokenizer=LLM_MODEL_NAME
    )

    llm = ChatHuggingFace(pipeline=hf_pipe, temperature=0.2)

    # Chain for combining documents and sending to LLM
    stuff_chain = StuffDocumentsChain(
        llm_chain=LLMChain(llm=llm, prompt=PROMPT),
        document_variable_name="context",
        return_only_outputs=True
    )

    def run_pipeline(query_type_key, question):
        query_type = QUERY_TYPES.get(query_type_key, "General")
        docs = retriever(question)
        context_text = "\n".join([f"{doc.page_content} (Source: {doc.metadata.get('source', 'Unknown')})" for doc in docs])
        result = stuff_chain.run({
            "query_type": query_type,
            "question": question,
            "context": context_text
        })
        return result

    return run_pipeline

# -------------------------------
# MAIN INTERACTIVE MENU
# -------------------------------
if __name__ == "__main__":
    # Load and process PDFs (only once)
    pdf_docs = load_documents()
    split_docs = split_documents(pdf_docs)
    create_chroma_vectorstore(split_docs)

    # Run pipeline
    pipeline = create_pipeline_chain()
    print("Welcome to Krishi AI Assistant")
    print("Select Query Type:")
    for k, v in QUERY_TYPES.items():
        print(f"{k}. {v}")
    
    choice = input("Enter choice number: ").strip()
    question = input("Enter your question: ").strip()
    answer = pipeline(choice, question)

    print("\n[FINAL ANSWER]:\n", answer)
