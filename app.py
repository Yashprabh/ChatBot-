import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI


# Load API key from .env file
OPENAI_API_KEY = "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"


#Upload pdf files
st.header('My First chatbot')

with st.sidebar:
    st.title("Your document")
    file = st.file_uploader("Upload a pdf file and start asking question",type="pdf")

#Extract the text
if file is not None:
    pdf_reader = PdfReader(file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()



#break it into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    #st.write(chunks)

#generating embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    #creating vector store-h
    vector_store = FAISS.from_texts(chunks,embeddings)

    #get user question
    user_question = st.text_input("Type your question here")

    #do similarity search
    if user_question:
        match = vector_store.similarity_search(user_question)
        #st.write(match)

        llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            temperature = 0,
            max_tokens = 1000,
            model_name = "gpt-3.5-turbo"
        )

        #output results
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match,question =  user_question)
        st.write(response)





