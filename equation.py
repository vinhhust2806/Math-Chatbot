from plot import *
import sympy as sp
import streamlit as st
import streamlit_antd_components as sac
from st_pages import add_page_title

st.set_option('deprecation.showPyplotGlobalUse', False)

if 'equation' not in st.session_state:
        st.session_state.equation = ''

def update_equation(char):
        st.session_state.equation += str(char)

def clear_equation():
        st.session_state.equation = ''

def main():
    add_page_title()

    with st.form(key='calculator_form'):
      with st.expander("Keyboard"):
       b = sac.buttons([
    sac.ButtonsItem(label='√', color='#25C3B0'), 
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

      if b == 0:
        update_equation('√')
    
      if b == 1:
        update_equation('∫')
    
      if b == 2:
        update_equation('∑')
    
      if b == 3:
        update_equation("∏")
    
      if b == 4:
        update_equation("∩")
     
      if b == 5:
        update_equation('∪')

      if b == 6:
        update_equation('⊂')
   
      if b == 7:
        update_equation('⊃')
 
      if b == 8:
        update_equation("∈")
   
      if b == 9:
        update_equation("⊖")
   
      if b == 10:
        update_equation('∆')
   
      if b == 11:
        update_equation('⊄')
   
      if b == 12:
        update_equation('⊅')

      if b == 13:
        clear_equation()

      st.write(f'<p style="color:black; font-style:italic; font-weight:bold;">❓ Equation:</p>', unsafe_allow_html=True)
      equation_input = st.text_input("Enter your message here:", label_visibility = "collapsed", placeholder="Enter what you want to caculate of know about")
      calculate_button = st.form_submit_button(label="Solve", help="Click to calculate")
      
    if calculate_button:
        try:
          if calculate_button:
            equation = sp.sympify(equation_input)
            solution = solve_equation(equation)

            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Input</p>', icon='house', align='start', size='sm', color='black')
            
            try:
               equation = sp.sympify(equation)
               equation_latex = sp.latex(equation)
               st.latex(equation_latex)

            except Exception as e:
               st.error(f"Error parsing equation: {e}")

            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Solution</p>', icon='house', align='start', size='sm', color='black')
             
            for i in range(len(solution)):
                st.write(f"Solution {i}: {solution[i]}")

            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Plot</p>', icon='house', align='start', size='sm', color='black')
            plot_equation(equation, solution)

            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Derivative</p>', icon='house', align='start', size='sm', color='black')
            derivative = calculate_derivative(equation)
            st.write(derivative)
            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Plot Derivative</p>', icon='house', align='start', size='sm', color='black')
            plot_derivative(derivative)

            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Primitive</p>', icon='house', align='start', size='sm', color='black')
            primitive = calculate_primitive(equation)
            st.write(primitive)
            sac.divider(label=f'<p style="color:black; font-style:italic; font-weight:bold; font-size:15px">Plot Primitive</p>', icon='house', align='start', size='sm', color='black')
            plot_primitive(primitive)
            
          else:
            st.write("Please enter an equation.")
        except:
          st.write("Please enter the right format of your equation.")  

if __name__ == "__main__":
     
    main()
