import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

from tracker import add_expense, expense_head, summary, plot_summary, monthly_expenses
df = pd.read_csv('expenses.csv')
monthly_expenses(df)
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