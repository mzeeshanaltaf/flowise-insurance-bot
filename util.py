import streamlit as st
from flowise import Flowise, PredictionData
import json
import requests
import tempfile
import os

def get_file_path(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name
        filename, _ = os.path.splitext(uploaded_file.name)
        return temp_pdf_path, filename

def upsert_documents_pinecone(uploaded_file):

    file_path, file_name = get_file_path(uploaded_file)

    form_data = {
        "files": (file_path, open(file_path, 'rb'))
    }
    body_data = {
        "pineconeNamespace": st.session_state.pinecone_namespace,
    }
    with st.spinner('Upserting Document in Vector DB ...'):
        _ = requests.post(st.secrets["UPSERT_URL"], files=form_data, data=body_data)
        st.success('Document Upserted Successfully!')

def generate_response(question: str, client):
    completion = client.create_prediction(
        PredictionData(
            chatflowId=st.secrets['CHATFLOW_ID'],
            question=question,
            overrideConfig={
                "sessionId": f"session_streamlit_{st.session_state.session_id }",
                "pineconeNamespace": st.session_state.pinecone_namespace
            },
            streaming=True
        )
    )

    for chunk in completion:
        parsed_chunk = json.loads(chunk)
        if parsed_chunk['event'] == 'token' and parsed_chunk['data'] != '':
            yield str(parsed_chunk['data'])

def display_footer():
    footer = """
    <style>
    /* Ensures the footer stays at the bottom of the sidebar */
    [data-testid="stSidebar"] > div: nth-child(3) {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
    }

    .footer {
        color: grey;
        font-size: 15px;
        text-align: center;
        background-color: transparent;
    }
    </style>
    <div class="footer">
    Made with ❤️ by <a href="mailto:zeeshan.altaf@gmail.com">Zeeshan</a>.
    </div>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)