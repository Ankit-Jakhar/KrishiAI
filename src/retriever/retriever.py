from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.schema import Document

from langdetect import detect
import os
import torch
torch.set_num_threads(4)  # Limit threads
device = "cpu"



load_dotenv()

API_KEY =os.getenv("GOOGLE_API_KEY")

CHROMA_DIR = "F:/KrishiAI/db/chroma"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

Prompt_Template =  """You are an agriculture expert assistant. 
Answer the farmer's query **clearly, concisely, and practically** using the provided documents.  
If the context is not sufficient, mention that explicitly but also give general agriculture knowledge.  

Question: {question}  
Context:  
{context}  

Answer in the same language as the question (Hindi or English).  
Provide a structured answer with bullet points if needed.
"""


Prompt =PromptTemplate(
    input_variables=["context", "question"],
    template=Prompt_Template
    
)

EMBEDDING_MODEL =  "sentence-transformers/all-MiniLM-L6-v2"



embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL ,model_kwargs={"device": "cpu"})
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_type="mmr" ,search_kwargs={"k": 3})


llm =ChatGoogleGenerativeAI(model="gemini-1.5-flash")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff", 
    chain_type_kwargs={"prompt": Prompt},# simplest type
    return_source_documents=False,
     input_key="query"
)
question= "Organic solution for aphid control in mustard."

def get_answer(question: str) -> str:
    response = qa_chain.invoke({"query": question})
    return response["result"]


 


