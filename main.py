import io
import fitz
from PIL import Image
import streamlit as st
from st_chat_message import message
import streamlit_antd_components as sac
from streamlit_cropper import st_cropper
from streamlit_login_auth_ui.widgets import __login__
from st_pages import add_page_title
from utils_template import process_uploaded_files, crop_pdf
from utils import answer, answer_step, answer_python, answer_context

if "messages" not in st.session_state:
    st.session_state.messages = []

if 'equation' not in st.session_state:
        st.session_state.equation = ''

def clear_history():
    st.session_state.user = []
    st.session_state.assistant = []

def update_equation(char):
        st.session_state.equation += str(char)

def clear_equation():
        st.session_state.equation = ''   

def chat_bot():
   if 'user' not in st.session_state:
     st.session_state.user = []

   if 'assistant' not in st.session_state:
     st.session_state.assistant = []

   message(
            "Hello, How can I help you?"    
        )
   
   with st.sidebar:
     if st.button("Clear Chat History"):
          clear_history()

   question = st.chat_input("Enter your question")

   if question:
          st.session_state.user.append(question)
          st.session_state.assistant.append(answer(question).strip())

   for i in range(len(st.session_state.assistant)):   
          message(st.session_state.user[i], is_user=True)
          message(st.session_state.assistant[i])

def math_deal():
  with st.form(key='calculator_form'):
   with st.expander("Keyboard"):
     b = sac.buttons([
    sac.ButtonsItem(label='\n√', color='#25C3B0'), 
    sac.ButtonsItem(label='∫', color='#25C3B0'),
    sac.ButtonsItem(label='∑', color='#25C3B0'),
    sac.ButtonsItem(label='∏', color='#25C3B0'),
    sac.ButtonsItem(label='∩', color='#25C3B0'),
    sac.ButtonsItem(label='∪', color='#25C3B0'),
    sac.ButtonsItem(label='⊂', color='#25C3B0'),
    sac.ButtonsItem(label='⊃', color='#25C3B0'),
    sac.ButtonsItem(label='∈', color='#25C3B0'),
    sac.ButtonsItem(label='⊖', color='#25C3B0'),
    sac.ButtonsItem(label='∆', color='#25C3B0'),
    sac.ButtonsItem(label='⊄', color='#25C3B0'),
    sac.ButtonsItem(label='⊅', color='#25C3B0'),
    sac.ButtonsItem(label='Del', color='#25C3B0'),
], label = '',align='start', size='xs', gap='xs', return_index=True)

   st.write( f'<p style="color:black; font-style:italic; font-weight:bold;">🔥 Hello, How can I help you!</p>', unsafe_allow_html=True)
   math_question = st.text_area("Enter your message here:", value= st.session_state.equation, label_visibility = "collapsed", placeholder="Enter math question you want to solve")
   calculate_button = st.form_submit_button(label="Submit", help="Click to submit")
  
  if calculate_button:
    a = answer_step(math_question).strip().split("\n\n")
    # Display question
    st.write(
            f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
            f'<p style="color:black; font-style:italic; font-weight:bold;">❓Question</p>'
            f'<p style="color:black; font-style:italic;">{math_question}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    # Display steps    
    for i in range(len(a)-1):
       sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Step{i+1}</p>', icon='house', align='start', size='sm', color='black')
       try:
           st.write(f'<p style="color:black; font-style:italic;">{a[i].split(f"Step {i+1}: ")[1]}</p>', unsafe_allow_html=True)
       except:
           st.write(f'<p style="color:black; font-style:italic;">{a[i]}</p>', unsafe_allow_html=True)
    # Display answer
    try:
       st.write(
            f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
            f'<p style="color:black; font-style:italic; font-weight:bold;">✏️Answer</p>'
            f'<p style="color:black; font-style:italic;">{a[-1].split(f"Step {i+2}: ")[1]}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    except:
       st.write(
            f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
            f'<p style="color:black; font-style:italic; font-weight:bold;">✏️Answer</p>'
            f'<p style="color:black; font-style:italic;">{a[-1]}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    # Rate
    a = sac.rate(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px;">Rate</p>', value=2.0, align='start')

    # Generate python code
    try: 
       code = answer_python(math_question).strip().split("python\n")[1]
    except:
       code = '''There no python code available'''
    # Display python code
    with st.expander("Python Code"):
       st.code(code, language='python')

def ask_pdf():
  with st.sidebar:
     img_file = st.file_uploader("Please upload your files for asking", type=['pdf'])
     st.info("Please refresh the browser if you decided to upload more files to reset the session", icon="🚨")

  if "context" not in st.session_state:
      st.session_state.context = []

  if img_file:
    st.write(
            f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
            f'<p style="color:black; font-style:italic; font-weight:bold;">✂️ Crop the questions you would like to ask! </p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    pdf_document = fitz.open(img_file)
    pix = pdf_document.load_page(0).get_pixmap()
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    cropped_img, crop_coords = st_cropper(img, realtime_update=True, box_color='black',
                                aspect_ratio=(1,1), return_type='both')
    left, top, width, height = crop_coords['left'], crop_coords['top'], crop_coords['width'], crop_coords['height']
    st.write("Preview Cropped Question")
    _ = cropped_img.thumbnail((300,300))
    st.image(cropped_img)

    crop = st.button("Crop")

    if crop:
             output_pdf = "cropped_new_file.pdf"
             crop_pdf(img_file, output_pdf, left, top, width, height)
             st.session_state.context.append(process_uploaded_files([output_pdf])[0][0])
    
  question = st.chat_input("Enter your question here:")

  if question:
        response_p = answer_context(question, st.session_state.context[-1]).strip()
        print(st.session_state.context)
        st.write(
              f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
              f'<p style="color:black; font-style:italic; font-weight:bold;">✏️Answer</p>'
              f'<p style="color:black; font-style:italic;">{response_p}</p>'
              f'</div>',
              unsafe_allow_html=True
             )       

def main(): 
 add_page_title()
 
 option = sac.tabs([
    sac.TabsItem(label=" ✏️ Solve Math Question"),
    sac.TabsItem(label=" 📖 Talk to Chatbot"),
    sac.TabsItem(label=" 📐 Ask the PDF File")
 ], align='start', return_index=True, size='xs')

 if option == 0:
    math_deal()

 if option == 1: 
    chat_bot()

 if option ==2:
    ask_pdf()

if __name__ == "__main__":
    __login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Log Out', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()

    if LOGGED_IN == True:
      main()