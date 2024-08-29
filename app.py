import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import bs4
from langchain.document_loaders import PDFPlumberLoader, TextLoader
import requests
# import validators

API = "AIzaSyBIvw7QEbrnN7HJTBqxu6CI_r7egCWf5tU"

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="""you are a helpfull AI assistant with main task to summarize documents
    you will take a text and summarize it to focus on the important topics
    you may get questions on the summarized topice you need you answer all of them
    text:{quesion}"""),
    ]

if "chat" not in st.session_state:
    st.session_state.chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API, temprature=0)

def web_scrap(url):
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.content, "html.parser")
  paragraphs = soup.find_all("p")
  doc = ""
  for p in paragraphs:
      doc += p.text
  return doc

def file_scrap(path):
  if path.split('.')[1] == "pdf":
    loader = PDFPlumberLoader(path)
  else:
    loader = TextLoader(path)
  doc = loader.load()
  d = ""
  for i in doc:
    d += i.page_content
  return d

def summarize(m, type="message"):
    st.session_state.messages.append(HumanMessage(content=m))
    answer = st.session_state.chat(st.session_state.messages)
    if type !="message":
        del st.session_state.messages[-1]
    st.session_state.messages.append(answer)
    return answer.content

def chatting(type="message", link="", path="", message=""):
    if type == 'link':
      doc = web_scrap(link)
      answer = summarize(doc, type=type)
    elif type =="file":
      doc = file_scrap(path)
      answer = summarize(doc, type=type)
    elif type =="message":
      answer = summarize(message, type=type)
    return answer

st.columns([1,1,1])[1].image("chatbot.png")
st.header("Octobot")
st.info("Easy Summarize your text documents, Web contents, LinkedIn posts, pdf, and text files...")

# for m in st.session_state.messages:
#     with st.chat_message(m['role']):
#         st.markdown(m['content'])
st.sidebar.info("Octobot")
st.sidebar.write("Summarize from:")
link = st.sidebar.text_input("Link")
st.sidebar.write("---")
file = st.sidebar.file_uploader("Browse Files...", type=["pdf", "txt"])

for m in st.session_state.messages:
    if m.type == "system":
        continue
    if m.type == "human":
        st.chat_message("user").markdown(m.content)
    else:
        st.chat_message("assistant").markdown(m.content)

message = st.chat_input("Say something")

if message is None:
    pass
else:
    st.chat_message("user").markdown(message)
    answer = chatting(message=message)
    st.chat_message("assistant").markdown(answer)

if file is not None:
    with open(file.name, 'wb') as f:
        f.write(file.getbuffer())
    answer = chatting(type='file', path=file.name)
    st.chat_message("assistant").markdown(answer)
    del file
if link is not "":
    # is_valid = validators.url(link)
    # if is_valid:
    answer = chatting(type="link", link=link)
    st.chat_message("assistant").markdown(answer)
    # else:
        # print("Invalid URL")
