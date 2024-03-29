from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import requests
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
safety_settings_NONE=[
    { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
    { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
    { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
    { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]
llm = GoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)
llm.client = genai.GenerativeModel(model_name='gemini-pro', safety_settings=safety_settings_NONE)

if "data" not in st.session_state:
    st.session_state.data = []
def validate_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.MissingSchema:
        return False
    except Exception as e:
        return False

def split_docs(documents, chunk_size=1000, chunk_overlap=100):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

def preprocess(url):
    loader = WebBaseLoader(url)
    documents=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=2000)
    docs = text_splitter.split_documents(documents)
    docs = split_docs(documents)
    return docs

def user_input(url,user_question):
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    documents=preprocess(url)
    docs = split_docs(documents)
    response = chain(
    {"input_documents":docs, "question": user_question}
    , return_only_outputs=True)
    return (response)


st.set_page_config("News summary")
st.header("News summarization chat using Gemini💁")
with st.form("my_form"):
   st.write("Provide Link and Chat")
   link = st.text_input("News Article link",placeholder="Enter link",key="link")
   question = st.text_input("Chat",placeholder="Enter chat",key="question")
   if st.form_submit_button('Submit'):
        if link=="" or question=="":
            st.error("Looks There is empty fields..!")
        else:
            if not link.startswith('http://') and not link.startswith('https://'):
                link = 'https://' + link
            if validate_url(link):
                with st.spinner("Processing..."):
                        res=user_input(link,question)
                        st.session_state.data.append({"link": link, "chat": question, "response": res["output_text"]})
                        st.write(res["output_text"])
            else:
                st.error("Invalid URl")

# Display the stored data
st.subheader("Previous Links, Chats, and Responses")
for item in st.session_state.data:
    st.subheader(f"Article: {item['link']}")
    st.write(f"Chat: {item['chat']}")
    st.write(f"Response: {item['response']}")
    st.write("---")