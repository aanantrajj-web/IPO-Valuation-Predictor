import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP ---
st.set_page_config(page_title="IPO Predictor", layout="centered")
st.title("📈 Real-World IPO Valuation Predictor")
st.write("Enter financial metrics, share count, and market sentiment to calculate a real-world IPO price.")

# --- TRAINING DATA & MODEL (Hidden in background) ---
data = {
    'Revenue': [3000, 25000, 250, 20000, 500, 804],
    'Profit Margins': [12, 15, -40, 8, -20, -11],
    'Cash Burn': [0, 0, 100, 0, 150, 90],
    'Total Valuation': [15000, 125000, 1200, 80000, 2500, 5500] 
}
df = pd.DataFrame(data)
X = df[['Revenue', 'Profit Margins', 'Cash Burn']]
y = df['Total Valuation']
model = LinearRegression()
model.fit(X, y)

# --- SECTION 1: FINANCIALS ---
st.markdown("### 📊 1. Core Financial Fundamentals")
company_name = st.text_input("Company Name", "e.g., Reddit")
revenue = st.number_input("Revenue (in millions)", value=804.0)
profit_margin = st.number_input("Profit Margins (%)", value=-11.0)
cash_burn = st.number_input("Cash Burn", value=90.0)

# Readiness Score Math
calculated_readiness = min(max(50 + (profit_margin * 2) + (revenue / 1000) - (cash_burn / 10), 0), 100)
st.info(f"**Calculated Market Readiness Score:** {calculated_readiness:.2f} / 100")

# Calculate Base Valuation (Done silently here so both buttons can use it)
input_data = pd.DataFrame([[revenue, profit_margin, cash_burn]], columns=['Revenue', 'Profit Margins', 'Cash Burn'])
base_valuation = max(model.predict(input_data)[0], 100) 

# --- BUTTON 1 ---
if st.button("Calculate Intrinsic Valuation (Fundamentals Only)"):
    st.success(f"### 🤖 ML Intrinsic Valuation: ${base_valuation:,.2f} Million")
    st.write("This is the raw, math-driven Total Company Valuation based *only* on financial fundamentals. It ignores market hype and share dilution.")

st.divider() # This adds a clean visual line break on the website!

# --- SECTION 2: REAL-WORLD MECHANICS ---
st.markdown("### 🏦 2. Real-World IPO Mechanics")
shares_offered = st.number_input("Total Shares Issued (in millions)", value=150.0)
market_sentiment = st.slider("Roadshow Hype Premium (1.0 = Neutral)", 0.5, 2.0, 1.2)
st.caption("Slide right for high brand demand (oversubscribed), slide left for cold market.")

# --- BUTTON 2 ---
if st.button("Calculate Final IPO Price (With Market Mechanics)"):
    final_valuation = base_valuation * market_sentiment
    ipo_price = final_valuation / shares_offered
    
    st.success(f"### 🎯 Final Predicted IPO Price for {company_name}: ${ipo_price:.2f} per share")
    
    st.write(f"**Under the hood math:**")
    st.write(f"- Base Intrinsic Valuation: **${base_valuation:,.2f} Million**")
    st.write(f"- Valuation after {market_sentiment}x Market Hype: **${final_valuation:,.2f} Million**")
    st.write(f"- Divided by {shares_offered} Million shares = **${ipo_price:.2f} / share**")
    st.balloons()