from PIL import Image
import streamlit as st
from utils import answer_context
from st_chat_message import message
from rapid_latex_ocr import LatexOCR
from st_pages import add_page_title

st.set_option('deprecation.showPyplotGlobalUse', False)
model = LatexOCR()

if 'user' not in st.session_state:
     st.session_state.user = []

if 'assistant' not in st.session_state:
     st.session_state.assistant = []

if 'context' not in st.session_state:
     st.session_state.context = []

def main():
    add_page_title()

    st.write(
            f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
            f'<p style="color:black; font-style:italic; font-weight:bold;">✏️ Upload your Equation Image to know about it!</p>'
            f'</div>',
            unsafe_allow_html=True
            )
    
    with st.sidebar:
        img_file = st.file_uploader("Please upload your files for asking", type=['png','jpg'])
        st.info("Please refresh the browser if you decided to upload more files to reset the session", icon="🚨")

    if img_file:
        with open(img_file.name, "rb") as f:
          question = f.read()
          formula, elapse = model(question)
          image = Image.open(img_file)
          st.image(image)
     
        col1, col2 = st.columns([1, 3])
        with col1:
               st.latex(formula)
        with col2:
               st.write('')
    
    question = st.chat_input("Enter your question")
    if question:
          st.session_state.user.append(question)
          st.session_state.assistant.append(answer_context(question, formula).strip())

    for i in range(len(st.session_state.assistant)):   
          message(st.session_state.user[i], is_user=True)
          message(st.session_state.assistant[i])
    
if __name__ == "__main__":
    main()
