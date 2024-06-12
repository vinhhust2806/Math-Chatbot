import streamlit as st
import streamlit as st
from st_pages import Page, show_pages, add_page_title
import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import fitz
import io
from utils_template import process_uploaded_files, crop_pdf
import streamlit_antd_components as sac
from st_chat_message import message
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from utils import response, response_python, response_pdf


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.user.append(user_input)
    st.session_state.chatbot.append(response_pdf(user_input).split(user_input)[1].strip())

def clear_history():
    st.session_state.user = []
    st.session_state.chatbot = []

def main(): 
 if "messages" not in st.session_state:
    st.session_state.messages = []
 add_page_title()
 show_pages(
        [
            Page("main.py", "Math Question", "🏠"),
            Page("visualize_equation.py", "Equation", ":bookmark_tabs:"),
            Page("OCR_equation.py", "Equation Image", ":books:"),
        ]
    )
 
 a = sac.tabs([
    sac.TabsItem(label=" ✏️ Solve Math Question"),
    sac.TabsItem(label=" 📖 Talk to Math Chatbot"),
    sac.TabsItem(label=" 📐 Ask the PDF File")
 ], align='start', return_index=True, size='xs')

 if a==0:
  if 'equation' not in st.session_state:
        st.session_state.equation = ''

    # Function to update the equation
  def update_equation(char):
        st.session_state.equation += str(char)

    # Function to clear the equation
  def clear_equation():
        st.session_state.equation = ''   
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
    a = response(math_question).split(math_question)[1].strip().split("\n\n")
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
       code = response_python(math_question).split(math_question)[1].strip().split("python\n")[1]
    except:
       code = '''There no python code available'''
    # Display python code
    with st.expander("Python Code"):
       st.code(code, language='python')
       
 elif a==2:
  with st.sidebar:
     img_file = st.file_uploader("Please upload your files for asking", type=['pdf'])
     st.info("Please refresh the browser if you decided to upload more files to reset the session", icon="🚨")

  question = st.text_input("Enter your question here:", label_visibility = "collapsed", placeholder="Enter what you want to ask about your file")
  
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
             context = process_uploaded_files([output_pdf])[0][0]
             #print(context)
             #with open(output_pdf, "rb") as file:
                 #st.download_button("Download Cropped PDF", file, file_name="new_cropped_pdf.pdf", mime="application/pdf")

             response_p = response_pdf(question + context).split(question + context)[1].strip()#.split("\n\n")
             st.write(
              f'<div style="background-color:white; padding:10px; border-radius:10px; border: 1px solid black;">'
              f'<p style="color:black; font-style:italic; font-weight:bold;">✏️Answer</p>'
              f'<p style="color:black; font-style:italic;">{response_p}</p>'
              f'</div>',
              unsafe_allow_html=True
             )
 else:
  
   st.session_state.setdefault(
    'user', 
    ['user']
   )
   st.session_state.setdefault(
    'chatbot', 
    ['chatbot']
    )
   st.session_state.setdefault(
    'chatbot1', 
    ['How can I help you?']
    )
   message(
            st.session_state['chatbot1'][0], 
            key=f"{500000}"     
        )
   for i in range(len(st.session_state['chatbot'])):   
        if st.session_state['user'][i]!= "user" and  st.session_state['chatbot'][i]!= "chatbot":         
          message(st.session_state['user'][i], is_user=True, key=f"{i}_user")
          message(st.session_state['chatbot'][i], key=f"{i}")
   with st.sidebar:
     if st.button("Clear Chat History"):
          clear_history()
   user_input = st.chat_input("Enter your question", on_submit=on_input_change, key="user_input")

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
