import numpy as np
import sympy as sp
import streamlit as st
import matplotlib.pyplot as plt

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
