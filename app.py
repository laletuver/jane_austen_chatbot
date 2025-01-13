import streamlit as st
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, Document
from llama_index.core.prompts.chat_prompts import ChatMessage, ChatPromptTemplate, MessageRole
from llama_index.embeddings.openai import OpenAIEmbedding
import openai
import os
import base64 


def set_bg_from_local(image_file: str):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
    }}
    </style> 
    """
    
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set your background (update path if needed)
set_bg_from_local("images/floral_background_1.png")

# Sidebar for OpenAI API key
with st.sidebar:
    st.header("🔑 Enter OpenAI API Key")
    openai_api_key = st.text_input("API Key", type="password", key="open_api_key")

    if st.button("Clear API Key"):
        st.session_state["open_api_key"] = ""  # Clear the key and reset input
        st.experimental_rerun()  # Restart the app without refreshing the page

 
# Validate API key
if not openai_api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

openai.api_key = openai_api_key


st.title("📜Jane Austen Chatbot")
st.markdown("""
<style>
.shadow-box {
    /* Box layout and positioning */
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    
     /* Semi-transparent white background and border */
    background-color: rgba(46, 44, 44, 0.9);
    border-radius: 5px;
    
    /* White text */
    color: #ffffff;
    font-size: 1rem;
    
    /* Dark box shadow */
    box-shadow: 0 4px 12px rgba(18, 16, 16, 0.8);
}
</style>

<div class="shadow-box">
    My name is Jane Austen, the writer of "Pride and Prejudice", "Emma", and other beloved novels.
    I am at your service. Pose any inquiry about literature, society, or the arts in my Regency world.
</div>
""", unsafe_allow_html=True)

st.image("images/jane_austen.png", caption="Portrait of Jane Austen", use_container_width=True)


# Embedding model setup
embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=openai_api_key  
)

# Load indexed files
@st.cache_data
def create_retrieve_index(index_path):
    if os.listdir(index_path) == []:
        st.warning("No index found. Please ensure that your files are correctly indexed.")
        st.stop()

    # Load from existing index
    storage_context = StorageContext.from_defaults(persist_dir=index_path)
    index = load_index_from_storage(storage_context=storage_context)
    return index

# Set directory for indexed documents
PERSIST_DIR = "./janeaustentext_index/"
VECTORINDEXDIR = os.path.join(PERSIST_DIR, 'VectorStoreIndex')

# Load index
vectorstoreindex = create_retrieve_index(VECTORINDEXDIR)

# Jane Austen's custom prompt
CUSTOM_PROMPT = [
    ChatMessage(
        content=(
            "You are Jane Austen, the celebrated author of works such as *Pride and Prejudice,* "
            "*Sense and Sensibility,* and *Emma.* Renowned for your wit, charm, and keen observations "
            "of Regency-era society, you respond as though you are living in the early 19th century, "
            "maintaining grace, elegance, and eloquence.\n\n"
            
            "### Rules for Responses ###\n"
            "1. **Tone and Style:** Your tone must always be warm, polite, and thoughtful, with occasional humor or irony. "
            "Your responses should reflect the stylistic flourishes characteristic of your novels.\n"
            "2. **Letter Format:** Frame your responses like letters, beginning with a warm salutation like my dear friend and ending with a warm closing.\n"
            "3. **Document Access:** You have access to documents containing your works, letters, and relevant writings. "
            "Ground your answers in these materials.\n"
            "4. **Era Accuracy:** Limit your answers to the knowledge, culture, and norms of the Regency era.\n\n"
            
            "### Topics You Can Discuss ###\n"
            "- Your own works\n"
            "- Literature and poetry\n"
            "- Social etiquette and fashion\n"
            "- Daily life and social customs\n"
            "- Arts and music\n\n"
            
            "### Restrictions ###\n"
            "- Refrain from answering questions about events, inventions, or terms from the 19th century onward. Simply state that you have no knowledge of such matters without elaboration.\n"
            "- Avoid using modern terminology, concepts, or references.\n"
            
            "### Behavior ###\n"
            "1. Always stay in character as Jane Austen.\n"
            "2. Do not acknowledge that you are an AI or assistant.\n"
            "3. Be engaging and articulate but also concise and informative.\n" 
            
            "### Example Interaction ###\n"
            "User Query: {query_str}\n"
            "Answer: "
        ),
        role=MessageRole.USER,
    ),
]

CHAT_PROMPT = ChatPromptTemplate(message_templates=CUSTOM_PROMPT)

# Create chat engine
chat_engine = vectorstoreindex.as_chat_engine(
    chat_mode="condense_question",
    context_window_size=5,
    verbose=True,
    text_qa_template=CHAT_PROMPT,
)

# Initialize chat session
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "My dear friend, I stand ready to converse on any matter you wish!"}]

theme_mode = st.get_option("theme.base")  # Get current theme (light or dark mode)
text_color = "white" if theme_mode == "dark" else "black"  # Set text color based on theme

for msg in st.session_state["messages"]:
    role_label = "You" if msg["role"] == "user" else "Jane Austen"
    st.markdown(
        f"<p style='color:{text_color}; font-size:16px;'><strong>{role_label}:</strong> {msg['content']}</p>",
        unsafe_allow_html=True
    )

# User message input
if prompt := st.chat_input("Your message..."):
    if not openai_api_key:
        st.warning("Please enter an OpenAI API key.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get Jane Austen's response
    response = chat_engine.chat(prompt)
    if not response.response:
        response_text = "I am unsure how to respond to that query, my dear friend."
    else:
        response_text = response.response

    st.session_state["messages"].append({"role": "assistant", "content": response_text})
    st.chat_message("assistant", avatar="🖋").write(response_text)


