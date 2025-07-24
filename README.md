# Octobot - Smart Summarizer

Scrapping and summaryzing text, pdf and text document files, web contents, LinkedIn posts, pdf, and YouTube videos content.

**Project Link**:
[Link](https://octobot.streamlit.app/)

## Key Points
- Scrapping web pages to get web content.
- Scrapping YouTube videos links to get text subtitles in Arabic or English languages.
- Scrapping text files (PDF & Text) to get text content.
- Summarizing the text contents using smart chatbot with message history based on LLM model (Google Gemini) using Langchain, focus on the important notes, and adding Q/A.
- Chatbot can talking to the users, summarizing text messages, answering questions on the summarized contents, and can help users to use the web page explaining step by step.
- Designed a user friendly graphical interface using Streamlit.

---

## 🧠 Tech Stack

- **Graphical Interface**: Streamlit
- **Backend**: Python
- **LLM**: Google Gemini (gemini-2.5-flash)
- **Other Libraries**: langchain, sentence_transformers, beautiful_soup, youtube_transcript_api, validators.

---
<!--
## 📂 Project Structure

```
Smart-ATS/
├── .streamlit/ # Streamlit config files
├── Data/ # Data-related folders
│ ├── job_description/ # Sample or scraped job description texts
│ └── vector_db/ # Vector database files (Chroma DB)
├── images/ # Visual assets and screenshots
├── notebooks/ # Jupyter notebooks for experimentation
├── .gitattributes # Git settings
├── README.md # Project documentation
├── Retriever.py # Core retrieval logic for RAG
├── requirements.txt # Python dependencies
└── st_app.py # Streamlit app entry point
```

---
-->

## 🚀 Getting Started

### 🔧 Prerequisites

Install required packages:
`pip install -r requirements.txt`

Run the app:
`streamlit run app.py`

---

## Screenshots
🎬 [Watch the Demo Video](https://drive.google.com/file/d/114VXBHbowapdFN8XHSlGwLOKbcWkFiJ9/view?usp=sharing)

<iframe src="https://drive.google.com/file/d/114VXBHbowapdFN8XHSlGwLOKbcWkFiJ9/preview" width="640" height="480" allow="autoplay"></iframe>

---

## Contact

Developed by Abdallah Fekry

📧 abdallahfekry95@gmail.com

🌐 [LinkedIn](https://www.linkedin.com/in/abdallah-fekry) | [GitHub](https://github.com/BeboFekry?tab=repositories)
