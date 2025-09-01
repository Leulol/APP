import os #Provides functions to interact with your operating system
import matplotlib
matplotlib.use('Qt5Agg')   # you can also try 'Qt5Agg' if TkAgg doesn't work
import pandas as pd #is a library for working with tables of data
import matplotlib.pyplot as plt #Used to create plots and charts
from datetime import datetime #Provides date and time functions. Here, we use it to get the current date when adding an expense

df = pd.read_csv('expenses.csv')

def add_expense(date, category, amount, note):
    global df
    df = pd.read_csv('expenses.csv')
    
    new_expense = pd.DataFrame({
        'Date': [date],
        'Category': [category],
        'Amount': [amount],
        'Note': [note]
    })
    
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv('expenses.csv', index=False)
    print("Expense added successfully.")

def expense_head():
    df = pd.read_csv("expenses.csv")
    print("Expenses Data:")
    print(df.head())

def summary(df):
    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
    summary = df.groupby("Category")["Amount"].sum()
    print("Summary by Category:")
    print(summary)

def plot_summary(df):
    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
    summary = df.groupby("Category")["Amount"].sum()
    summary.plot(kind="bar", title="Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.show()

def monthly_expenses(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
    
    monthly.plot(kind="bar", title="Monthly Expenses", rot=45)
    plt.xlabel("Month")
    plt.ylabel("Total Amount")
    plt.tight_layout()
    plt.show()

