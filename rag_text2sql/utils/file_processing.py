from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import tempfile, os

def process_pdf(uploaded_file, openai_api_key):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    pages = loader.load_and_split()

    for i, page in enumerate(pages):
        page.metadata["source"] = uploaded_file.name
        page.metadata["page_number"] = i + 1

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings(api_key=openai_api_key, model="text-embedding-3-small")
    vector_db = FAISS.from_documents(chunks, embeddings)
    os.remove(tmp_path)
    return vector_db
