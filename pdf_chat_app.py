import streamlit as st
import fitz  # pip install PyMuPDF
import openai

# -----------------------------
# CONFIG
# -----------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"  # replace with your API key

st.set_page_config(page_title="PDF Chat Assistant", layout="wide")
st.title("📄 PDF Chat Assistant")

# -----------------------------
# PDF Upload
# -----------------------------
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

if pdf_file:
    if "pdf_text" not in st.session_state:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        st.session_state["pdf_text"] = text
        st.session_state["chat_history"] = []
        st.success("PDF loaded successfully! You can now ask questions.")

# -----------------------------
# Chat Interface
# -----------------------------
if "pdf_text" in st.session_state:
    user_input = st.text_input("Ask a question about the PDF:")

    if st.button("Send") and user_input:
        # Add user message to chat history
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        # Prepare GPT messages
        system_prompt = f"You are a helpful assistant. Answer questions based on the following PDF content:\n{st.session_state['pdf_text']}"
        messages = [{"role": "system", "content": system_prompt}] + st.session_state["chat_history"]

        # Call GPT API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )

        assistant_message = response['choices'][0]['message']['content']

        # Add assistant reply to chat history
        st.session_state["chat_history"].append({"role": "assistant", "content": assistant_message})

    # Display chat
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")
