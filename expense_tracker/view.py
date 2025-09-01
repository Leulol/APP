import streamlit as st
import pandas as pd
import numpy as np
st.title("Expense Tracker")
st.write("Welcome — this page shows your expenses.")
st.header("Quick Notes")
"""
# My first app
Here's our first attempt at using data to create a table:
"""

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))


dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
st.write(np.random.randn(10,20))




