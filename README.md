# 📜 Jane Austen Chatbot

Welcome to the **Jane Austen Chatbot**. It is a **Streamlit-based application** that allows you to have a conversation with Jane Austen. This chatbot generates Jane Austen's responses in her  **Regency-era tone** using OpenAI’s GPT models and references her writings, life and letters.

https://janeaustenchatbot.streamlit.app

---

## **📝 Features**
- **Conversational AI:** Chat with Jane Austen. 
- **Custom Style:** Responses are framed as polite and witty letters in the Regency style.
- **Contextual Answers:** Responses are grounded in Jane Austen’s actual works and letters as well as books written about her life and the Regency era. 
- **Document Indexing:** The chatbot retrieves information from preprocessed `.txt` files containing her works.

---

## **📂 Project Structure**

```plaintext
jane-austen-chatbot/
├── app.py                # Main Streamlit app
├── README.md             # Documentation
├── requirements.txt      # Dependencies (Python packages)
├── janeaustentext_index/  # Indexed files created by LlamaIndex (contains JSON index files)
└── works/                # Folder containing Jane Austen's writings, letters, books and articles about her life. 
    ├── pride_and_prejudice/
    │   └── chapter_1.txt
    ├── sense_and_sensibility/
    │   └── chapter_1.txt
    └── letters/
        └── letters_chapter_i.txt 
