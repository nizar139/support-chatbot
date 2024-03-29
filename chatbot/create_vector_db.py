# from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceHubEmbeddings

from config import vector_db_dir, documents_parent_dir

if __name__ == "__main__":
    loader = DirectoryLoader(documents_parent_dir, glob="documents/*.pdf")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)
    embeddings = HuggingFaceHubEmbeddings()
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory=vector_db_dir)

    ## test
    retriever = vectorstore.as_retriever(k=1)
    docs = retriever.invoke("who are Madkudu?")
    print(docs)

