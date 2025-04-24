import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from flowise import Flowise, PredictionData
from util import *
import uuid

# Page title of the application
page_title = "InsuranceGenie"
page_icon = "🧞‍♀️"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

# Application Title and description
st.title(f'{page_title}{page_icon}')
st.write('***:blue[Uncover Insights from Your Insurance Docs 📊]***')
st.write("""
Upload your insurance documents and ask questions. Get answers, insights, and clarity on your coverage. 📝
""")
# Display footer in the sidebar
display_footer()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I am InsuranceGenie. Your AI Assitant. How can I help you?"}]
if "response" not in st.session_state:
    st.session_state.response = None
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4()
if "pinecone_namespace" not in st.session_state:
    st.session_state.pinecone_namespace = None

# File uploader
st.subheader("Upload a Insurance File:", divider='gray')
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed")

# If pdf file is not none then save the contents of the pdf file into temp file
if uploaded_pdf is not None:
    upsert_button = st.button('Upsert', type="primary", icon=":material/upload_file:")

    if upsert_button:
        st.session_state.pinecone_namespace = f"streamlit_{uuid.uuid4()}"
        upsert_documents_pinecone(uploaded_pdf)

    col1, col2 = st.columns([.7, .3], vertical_alignment="top")

    client = Flowise(base_url=st.secrets['BASE_URL'])

    # Chat with document section
    col1.subheader('Ask the Genie:', divider='gray')
    for msg in st.session_state.messages:
        col1.chat_message(msg["role"]).write(msg["content"])

    if question := st.chat_input(placeholder='Ask InsuranceGenie ...', disabled=not st.session_state.pinecone_namespace):
        st.session_state.messages.append({"role": "user", "content": question})
        col1.chat_message("user").write(question)
        with st.spinner('💭Thinking...', show_time=True):
            response = generate_response(question, client)
            full_response = col1.chat_message("assistant").write_stream(response)
            st.session_state.response = full_response
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.response})

    # PDF Previewer section
    with col2:
        st.subheader('PDF Previewer:', divider='gray')
        with st.expander(':blue[***Preview PDF***]', expanded=False, icon=':material/preview:'):
            pdf_viewer(uploaded_pdf.getvalue(), height=500, render_text=True)


