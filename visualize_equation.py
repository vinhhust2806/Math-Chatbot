import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import streamlit_antd_components as sac
import streamlit as st 
from st_pages import Page, show_pages, add_page_title, Section
st.set_option('deprecation.showPyplotGlobalUse', False)


def solve_equation(equation):
    try:
        x = sp.symbols('x')
        solution = sp.solve(equation, x)
        return solution
    except Exception as e:
        return str(e)

def calculate_derivative(equation):
    x = sp.symbols('x')
    derivative = sp.diff(equation, x)
    return derivative

def calculate_primitive(equation):
    x = sp.symbols('x')
    primitive = sp.integrate(equation, x)
    return primitive

def plot_equation(equation, solution):
    x = np.linspace(-10, 10, 400)
    y = np.array([sp.lambdify('x', equation)(x_val) for x_val in x])

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='Original Equation')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of the Original Equation')
    if solution:
        for sol in solution:
            plt.plot(sol, sp.lambdify('x', equation)(sol), 'ro')
            plt.text(sol, sp.lambdify('x', equation)(sol), f'({sol}, {sp.lambdify("x", equation)(sol)})', fontsize=10, ha='right')
    plt.legend()
    st.pyplot()

def plot_derivative(derivative):
    x = np.linspace(-10, 10, 400)
    derivative_func = sp.lambdify('x', derivative)
    y_derivative = derivative_func(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y_derivative, label='Derivative')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of the Derivative')
    plt.legend()
    st.pyplot()

def plot_primitive(primitive):
    x = np.linspace(-10, 10, 400)
    primitive_func = sp.lambdify('x', primitive)
    y_primitive = primitive_func(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y_primitive, label='Primitive')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of the Primitive')
    plt.legend()
    st.pyplot()

if 'equation' not in st.session_state:
        st.session_state.equation = ''

def update_equation(char):
        st.session_state.equation += str(char)

def clear_equation():
        st.session_state.equation = ''
def main():

    add_page_title()
    show_pages(
        [
            Page("C:/chabot/main.py", "Math Question", "🏠"),
            Page("C:/chabot/visualize_equation.py", "Equation", ":bookmark_tabs:"),
            Page("C:/chabot/OCR_equation.py", "Equation Image", ":books:"),
        ]
    )

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
      st.write( f'<p style="color:black; font-style:italic; font-weight:bold;">❓ Equation:</p>', unsafe_allow_html=True)
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
