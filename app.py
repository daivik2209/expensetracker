import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File to store data
CSV_FILE = "tickets.csv"

# Load existing data or create new
required_columns = ["Match", "Stand", "Purchase Price", "Selling Price", "Quantity", "Profit"]

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    # Clean up any unwanted columns like "Unnamed: 0"
    df = df[[col for col in df.columns if col in required_columns]]
    # Add missing columns if needed
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
else:
    df = pd.DataFrame(columns=required_columns)
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
    new_row = {
        "Match": match,
        "Stand": stand,
        "Purchase Price": purchase_price,
        "Selling Price": selling_price,
        "Quantity": quantity,
        "Profit": profit
    }
    new_data = pd.DataFrame([new_row])
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

    # 💾 Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="tickets.csv", mime="text/csv")

    # 🚨 RESET DATA BUTTON
    st.warning("⚠️ After viewing, click below to reset all data.")
    if st.button("🔄 Reset Tracker"):
        df = pd.DataFrame(columns=required_columns)
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ All data erased! Ready to start fresh.")