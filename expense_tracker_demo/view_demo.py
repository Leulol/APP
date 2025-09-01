import streamlit as st#Interactive web apps
import pandas as pd#Dataframes
import random#Generate somthing random
import time#For countdown
import matplotlib.pyplot as plt#For plots
import numpy as np#For numerical operations
from sympy import symbols, sympify, lambdify, Eq, solve#Turn to Symbolic mathematics

# ---------------------------
# App Title
# ---------------------------
st.title("Expense Tracker")
st.write("Welcome — this page shows your expenses.")
st.header("Quick Notes")

"""
# My first app
Here's our first attempt at using data to create a table:
"""

# ---------------------------
# Slider example
# ---------------------------
x_slider = st.slider('Select a number')
st.write(x_slider, 'squared is', x_slider * x_slider)

# ---------------------------
# DataFrames for expenses
# ---------------------------
dataframe = {
    'first': pd.DataFrame({
        'Dates': [2023, 2024, 2025, 2026],
        'Amounts': [100, 200, 300, 400]
    }),
    'second': pd.DataFrame({
        'Dates': [2026, 2025, 2024, 2023],
        'Amounts': [400, 300, 200, 100]
    })
}

if st.checkbox('first'):
    st.write(dataframe['first'])
if st.checkbox('second'):
    st.write(dataframe['second'])

# ---------------------------
# Sidebar inputs
# ---------------------------
name = st.sidebar.text_input('Your name', placeholder='Type here...')

options = ('Email', 'Home phone', 'Mobile phone')
contact_method = st.sidebar.selectbox('How would you like to be contacted?', options)

if contact_method == "Email":
    email = st.sidebar.text_input("Enter your email address")
    if email and "@gmail.com" not in email:
        st.write("Please enter a valid email address.")
    elif email:
        st.write(f"We'll contact {name} at: {email}")
elif contact_method in ("Home phone", "Mobile phone"):
    phone = st.sidebar.text_input("Enter your phone number")
    if phone:
        try:
            phone_int = int(phone)
        except ValueError:
            st.write("Please enter a valid phone number.")
        else:
            st.write(f"We'll contact {name} at: {phone_int}")

# Slider to generate random number
value = st.sidebar.slider(
    'Select a range of values',
    min_value=0.0,
    max_value=100.0,
    value=(25.0, 75.0)
)
st.sidebar.write("Do you want to generate a random number using the above domain?")
if st.sidebar.button('Generate'):
    low = int(value[0])
    high = int(value[1])
    st.sidebar.write(random.randint(low, high))

# Hogwarts house selector
house = st.sidebar.radio(
    'Sorting hat',
    ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
)
st.sidebar.write(f"You are in {house} house!")

# ---------------------------
# Sleep button with progress bar
# ---------------------------
sleep_time = st.text_input("Enter number of seconds to sleep", placeholder="Type here...")

if 'sleep_count' not in st.session_state:#?
    st.session_state['sleep_count'] = 0
if 'bar_value' not in st.session_state:
    st.session_state['bar_value'] = 0

latest_iteration = st.empty()
bar = st.progress(st.session_state['bar_value'])

if st.button('Sleep', key='sleep_button'):
    try:
        secs = int(sleep_time)
        if secs < 0:
            raise ValueError
    except ValueError:
        st.error('Please enter a valid positive integer number of seconds')
    else:
        for i in range(secs):
            time.sleep(1)
            st.session_state['bar_value'] = min(100, st.session_state['bar_value'] + int(100/secs))
            bar.progress(st.session_state['bar_value'])
        st.session_state['sleep_count'] += 1
        latest_iteration.text(f"Iteration {st.session_state['sleep_count']}")
        st.write("Waki Waki!")

# ---------------------------
# Cartesian Plot Section
# ---------------------------
equation = st.text_input("Enter your equation here", placeholder="e.g., x**2 - 5*x + 6")
x_symbol = symbols('x')

if equation:
    try:
        expr = sympify(equation)
        y_func = lambdify(x_symbol, expr, 'numpy')

        # Create x values and y values for plotting
        x_vals = np.linspace(-10, 10, 400)
        y_vals = y_func(x_vals)

        mode = st.radio("Choose mode", ("Normal", "Slider", "Y-value"))

        # --- PLOT ---
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f"y = {equation}")

        if mode == "Normal":
            # User types an x value
            x_point = st.number_input("Select x value", min_value=-10.0, max_value=10.0, value=0.0)
            y_point = y_func(x_point)
            ax.plot(x_point, y_point, "ro")
            ax.text(x_point, y_point, f"({x_point:.2f}, {y_point:.2f})")

        elif mode == "Slider":
            # User slides to pick x
            x_point = st.slider("Select x value", min_value=-10.0, max_value=10.0, value=0.0)
            y_point = y_func(x_point)
            ax.plot(x_point, y_point, "ro")
            ax.text(x_point, y_point, f"({x_point:.2f}, {y_point:.2f})")

        elif mode == "Y-value":
            # User enters y, solve for x
            mode_y = st.radio("Y-value mode", ("Normal", "Slider"))

            if mode_y == "Normal":
                y_point = st.number_input("Enter the y value", min_value=-10.0, max_value=10.0, value=0.0)
            else:
                y_point = st.slider("Select y value", min_value=-10.0, max_value=10.0, value=0.0)

            solutions = solve(Eq(expr, y_point), x_symbol)

            if solutions:
                for sol in solutions:
                    try:
                        x_point = float(sol.evalf())
                        ax.plot(x_point, y_point, "ro")
                        ax.text(x_point, y_point, f"({x_point:.2f}, {y_point:.2f})", fontsize=9, color="red")
                    except Exception:
                        pass
            else:
                st.warning("No solution found for this y value.")

        # Cross axes
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.legend()
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Invalid equation: {e}")
else:
    st.write(" Please enter an equation above.")