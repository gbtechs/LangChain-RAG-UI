import os

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.globals import set_debug
from langchain_community.vectorstores import FAISS

# import chromadb.utils.embedding_functions as embedding_functions

# openai_api_key = os.environ.get('OPENAI_API_KEY')
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=openai_api_key,
#                 model_name="text-embedding-3-small",
#             )

docx =[]
path_to_docx_folder = "KnowledgeBase"

print("###################### Hello From INIT ######################")
print("Docs Count: ",os.listdir(path_to_docx_folder))
for docx_file in os.listdir(path_to_docx_folder):
    if docx_file.endswith(".docx"):
        docx.append(os.path.join(path_to_docx_folder, docx_file))
        print("docx: ", os.path.join(path_to_docx_folder, docx_file))
print("DOCX: ",docx)

for file in docx:
    loader = Docx2txtLoader(file)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    print(len(splits))
    # Create an instance of OpenAIEmbeddings
    openai_embeddings = OpenAIEmbeddings()
    # Check if Chroma class instantiation is causing the issue
    try:
        chroma_instance = Chroma(embedding_function=openai_embeddings)
    except TypeError as e:
        print("Error during Chroma instantiation:", e)
    # Use Chroma.from_documents() with embedding_function parameter set once
    db = FAISS.from_documents(docs, OpenAIEmbeddings())

query = "I want to bring my own broker"
docs = db.similarity_search(query)
print(docs[0].page_content)