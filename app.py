import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File to store data
CSV_FILE = "tickets.csv"

# Load existing data or create new
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    required_columns = ["Match", "Stand", "Purchase Price", "Selling Price", "Quantity", "Profit"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
else:
    df = pd.DataFrame(columns=["Match", "Stand", "Purchase Price", "Selling Price", "Quantity", "Profit"])
    df.to_csv(CSV_FILE, index=False)

st.title("🏏 IPL Ticket Expense & Profit Tracker")

# Sidebar Form to Add New Ticket Data
st.sidebar.header("➕ Add New Ticket")
match = st.sidebar.text_input("Match Name")
stand = st.sidebar.text_input("Stand Name")
purchase_price = st.sidebar.number_input("Purchase Price", min_value=0.0)
selling_price = st.sidebar.number_input("Selling Price", min_value=0.0)
quantity = st.sidebar.number_input("Quantity", min_value=1, step=1)

if st.sidebar.button("Add Ticket"):
    profit = (selling_price - purchase_price) * quantity
    new_data = pd.DataFrame([[match, stand, purchase_price, selling_price, quantity, profit]], 
                            columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.sidebar.success("✅ Ticket added successfully!")

# Display Data
st.subheader("📜 Transaction History")
st.dataframe(df)

# Total Profit Calculation
total_profit = df["Profit"].sum()
st.subheader(f"💰 Total Profit: ₹{total_profit:.2f}")

# ---- 📊 Graphs ----
if not df.empty:
    st.subheader("📈 Profit Trends & Insights")

    # 📉 Profit Trend Over Time
    df["Cumulative Profit"] = df["Profit"].cumsum()
    st.line_chart(df["Cumulative Profit"])

    # 🏟️ Match-wise Sales & Profit
    match_summary = df.groupby("Match")[["Selling Price", "Profit"]].sum().reset_index()
    st.bar_chart(match_summary.set_index("Match"))

    # 📊 Stand-wise Profit Comparison
    stand_summary = df.groupby("Stand")["Profit"].sum().reset_index()
    st.bar_chart(stand_summary.set_index("Stand"))

    # 🎯 Profit Distribution (Pie)
    fig, ax = plt.subplots()
    df.groupby("Match")["Profit"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

    # 🚨 RESET DATA BUTTON
    st.warning("⚠️ After viewing, click below to reset all data.")
    if st.button("🔄 Reset Tracker"):
        df = pd.DataFrame(columns=df.columns)
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ All data erased! Ready to start fresh.")