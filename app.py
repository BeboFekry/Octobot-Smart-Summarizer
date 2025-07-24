import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import bs4
from langchain.document_loaders import PDFPlumberLoader, TextLoader
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import validators
from youtube_transcript_api.proxies import WebshareProxyConfig

st.set_page_config(page_title="Octobot", page_icon='images/chatbot.png')

st.columns([1,1,1])[1].image("images/chatbot.png", width=150)
st.columns([2.1,2,2])[1].header("Octobot")
st.info("Easy Summarize your text documents, Web contents, LinkedIn posts, pdf, and text files...")

if 'API' not in st.session_state:
  st.session_state.API = st.secrets["API"]
if "messages" not in st.session_state:
    with open("prompt.txt", 'r') as f:
      prompt = f.read()
    st.session_state.messages = [
        SystemMessage(content=prompt),
    ]

if "chat" not in st.session_state:
    st.session_state.chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=st.session_state.API, temprature=0)

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

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    return None

def youtube_scrapper(url):
  video_id = extract_video_id(url)
  try:
      username = st.secrets['proxy_username']
      password = st.secrets['proxy_password']
      ty_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
          proxy_username=username,
          proxy_password=password,
        )
      )
      transcript = ty_api.fetch(video_id, languages=['ar','en'])
      with open("subtitles.txt", "w", encoding='utf-8') as f:
          for entry in transcript:
              f.write(entry.text)
      with open("subtitles.txt", "r", encoding='utf-8') as f:
          return f.read()
  except Exception as e:
     return f"Error: {e}"

def summarize(m, type="message"):
    st.session_state.messages.append(HumanMessage(content=m))
    answer = st.session_state.chat(st.session_state.messages)
    # if type !="message":
    #     del st.session_state.messages[-1]
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
    elif type=="youtube_link":
      doc = youtube_scrapper(link)
      answer = summarize(doc, type=type)
    return answer

# st.sidebar.info("Octobot")
st.sidebar.write("**Summarize from:**")
web_link = st.sidebar.text_input("Webpage Link")
bt = st.sidebar.button("Summarize")
if bt and web_link=="":
   st.sidebar.error("Please enter web link!")
elif bt and not validators.url(web_link):
   st.sidebar.error("Error: Invalid web url!")
   web_link = ""
st.sidebar.write("---")
youtube_link = st.sidebar.text_input("YouTube Video Link")
bt_youtube = st.sidebar.button(" Summarize")
if bt_youtube and youtube_link=="":
   st.sidebar.error("Please enter youtube link!")
elif bt_youtube and not validators.url(youtube_link):
   st.sidebar.error("Error: Invalid youtube url!")
   youtube_link = ""
st.sidebar.write("---")
file = st.sidebar.file_uploader("Browse Files...", type=["pdf", "txt"])
bt_file = st.sidebar.button("Summarize ")

st.write('---')
for m in st.session_state.messages:
    if m.type == "system":
        continue
    if m.type == "human":
        if len(m.content)>500:
           continue
        else:
          st.chat_message("user").markdown(m.content)
    else:
        st.chat_message("assistant").markdown(m.content)

message = st.chat_input("Say something...")

if message is None:
    pass
else:
    st.chat_message("user").markdown(message)
    answer = chatting(message=message)
    st.chat_message("assistant").markdown(answer)
    st.write("---")

if bt_file:
    if file is not None:
        with st.spinner("Please wait, loading file content..."):
          with open(file.name, 'wb') as f:
              f.write(file.getbuffer())
          answer = chatting(type='file', path=file.name)
          st.chat_message("assistant").markdown(answer)
          del file
    else:
       st.sidebar.error("Please add pdf file!")

if bt:
    if web_link is not "":
        with st.spinner("Please wait, loading web content..."):
          answer = chatting(type="link", link=web_link)
          st.chat_message("assistant").markdown(answer)

if bt_youtube:
    if youtube_link is not "":
        with st.spinner("Please wait, loading YouTube content..."):
          answer = chatting(type="youtube_link", link=youtube_link)
          st.chat_message("assistant").markdown(answer)
