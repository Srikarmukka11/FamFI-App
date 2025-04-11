import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Authentication ---
def login():
    st.title("🔐 FamFi Login")
    pwd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pwd == "Sureshkrishna5445":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password. Try again.")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

# --- Core App ---
DATA_FILE = "famfi_data.csv"

def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Date", "Category", "Type", "Amount", "Note"])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_entry(date, category, ttype, amount, note):
    df = load_data()
    new_entry = pd.DataFrame([[date, category, ttype, amount, note]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def delete_entry(index):
    df = load_data()
    df.drop(index=index, inplace=True)
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="FamFi - Financial Tracker", layout="wide")
st.title("💰 FamFi - Offline Family Financial Tracker")

init_data_file()
data = load_data()

tab1, tab2, tab3 = st.tabs(["➕ Add Entry", "📊 View Data", "📉 Analysis"])

with tab1:
    st.header("Add Income / Expense")
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", ["Salary", "Food", "Transport", "Utilities", "Health", "Others"])
        ttype = st.selectbox("Type", ["Income", "Expense"])

    with col2:
        amount = st.number_input("Amount", min_value=0.0, step=0.5)
        note = st.text_input("Note (Optional)")

    if st.button("Add Entry"):
        save_entry(date, category, ttype, amount, note)
        st.success("✅ Entry Added!")

with tab2:
    st.header("View & Manage Entries")
    st.dataframe(data, use_container_width=True)

    if not data.empty:
        delete_index = st.number_input("Enter index of row to delete", min_value=0, max_value=len(data)-1, step=1)
        if st.button("Delete Entry"):
            delete_entry(delete_index)
            st.success(f"❌ Entry at index {delete_index} deleted.")
            st.rerun()
    else:
        st.info("No entries to delete.")

with tab3:
    st.header("Financial Analysis")

    total_income = data[data["Type"] == "Income"]["Amount"].sum()
    total_expense = data[data["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    st.metric("Total Income", f"₹{total_income:.2f}")
    st.metric("Total Expense", f"₹{total_expense:.2f}")
    st.metric("Balance", f"₹{balance:.2f}")

    st.subheader("Breakdown by Category")
    if not data.empty:
        breakdown = data.groupby(["Category", "Type"])["Amount"].sum().unstack(fill_value=0)
        st.bar_chart(breakdown)
    else:
        st.info("No data to display yet.")

# Signature
st.markdown("---")
st.markdown("Made with ❤️ by **Srikar Mukka**")
