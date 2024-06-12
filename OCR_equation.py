import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import streamlit_antd_components as sac
import streamlit as st 
from st_pages import Page, show_pages, add_page_title, Section
st.set_option('deprecation.showPyplotGlobalUse', False)
from rapid_latex_ocr import LatexOCR
from utils import response_pdf
model = LatexOCR()


def main():
    #st.title("Equation Solver, Derivative, and Primitive Calculator")
    #st.write("Enter your equation below:")
    add_page_title()
    show_pages(
        [
            Page("C:/chabot/main.py", "Math Question", "🏠"),
            Page("C:/chabot/visualize_equation.py", "Equation", ":bookmark_tabs:"),
            Page("C:/chabot/OCR_equation.py", "Equation Image", ":books:"),
        ]
    )
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
          data = f.read()

          res, elapse = model(data)
       
          st.latex(res)
          a = response_pdf(res).split(res)[1].strip()
          st.write(
            f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
            f'<p style="color:black; font-style:italic; font-weight:bold;">✏️Answer</p>'
            f'<p style="color:black; font-style:italic;">{a}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
if __name__ == "__main__":
     
    main()
