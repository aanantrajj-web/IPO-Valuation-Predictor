import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP ---
st.set_page_config(page_title="IPO Predictor Pro", layout="centered")
st.title("📈 Institutional IPO Valuation Engine")
st.write("This engine bridges quantitative machine learning with real-world investment banking mechanics to predict a highly accurate IPO price.")

st.divider()

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
st.header("Phase 1: Intrinsic Financial Fundamentals")
st.markdown("""
**📝 Investment Thesis:** Before factoring in market hype, a company has an *intrinsic* baseline value driven by its core financials. 
*   **Revenue:** Demonstrates market share and scale.
*   **Profit Margins:** Shows operational efficiency and pricing power.
*   **Cash Burn:** Highlights liquidity risk (high cash burn severely penalizes valuation).
""")

company_name = st.text_input("Company Name", "e.g., Reddit")
col1, col2, col3 = st.columns(3)
with col1:
    revenue = st.number_input("Revenue ($M)", value=804.0)
with col2:
    profit_margin = st.number_input("Profit Margin (%)", value=-11.0)
with col3:
    cash_burn = st.number_input("Cash Burn ($M)", value=90.0)

# Calculate Base Valuation 
input_data = pd.DataFrame([[revenue, profit_margin, cash_burn]], columns=['Revenue', 'Profit Margins', 'Cash Burn'])
base_valuation = max(model.predict(input_data)[0], 100) 

if st.button("Calculate Intrinsic Valuation"):
    st.success(f"### 🤖 ML Intrinsic Valuation: ${base_valuation:,.2f} Million")
    st.write("This is the raw Total Company Value based *only* on machine learning. It ignores market hype and share dilution.")

st.divider() 

# --- SECTION 2: SHARE DILUTION ---
st.header("Phase 2: Share Dilution (Cutting the Equity Pie)")
st.markdown("""
**📝 Investment Thesis:** A $10 Billion company is priced differently depending on how many pieces it is sliced into. Dividing the Total Valuation by the Number of Shares dictates the mathematical base share price.
""")

shares_offered = st.number_input("Total Shares Issued to Public (in millions)", value=150.0)

if st.button("Calculate Base IPO Price (No Hype)"):
    base_ipo_price = base_valuation / shares_offered
    st.success(f"### 📈 Base IPO Price: ${base_ipo_price:.2f} per share")

st.divider()

# --- SECTION 3: REAL-WORLD MECHANICS (QUANTIFIED ROADSHOW) ---
st.header("Phase 3: The Roadshow (Supply & Demand)")
st.markdown("""
**📝 Investment Thesis:** In real-world investment banking, an IPO price is heavily influenced by the "Roadshow"—the period where bankers pitch the stock to institutions. 
*Enter the real-world market metrics below, and the **Roadshow Premium Bar** will automatically calculate and deflect based on your inputs.*
""")

# The inputs that drive the bar
col_a, col_b = st.columns(2)
with col_a:
    shares_demanded = st.number_input("Total Shares Demanded by Investors ($M)", value=450.0)
    st.caption("If demand > supply, the price goes up.")
with col_b:
    sp500_return = st.number_input("S&P 500 YTD Return (%)", value=12.0)
    st.caption("A strong stock market allows for higher pricing.")

# The Math that drives the automatic bar
oversubscription = max(shares_demanded / shares_offered, 0.1) # Calculate how many times oversubscribed
oversub_mod = (oversubscription - 1.0) * 0.05 # Add 5% premium for every 1x oversubscribed

climate_mod = 0.15 if sp500_return >= 10 else (-0.15 if sp500_return <= 0 else 0.0)

# Calculate final automatic hype
calculated_hype = 1.0 + oversub_mod + climate_mod
calculated_hype = max(min(calculated_hype, 2.5), 0.5) # Keep between 0.5x and 2.5x

# --- THE AUTOMATIC BAR ---
st.write("### 📊 Automated Market Sentiment Bar")
st.slider("Calculated Hype Premium (1.0 = Neutral)", 0.5, 2.5, float(calculated_hype), disabled=True)
st.caption("🔒 *This bar is locked. It automatically deflects in real-time based on the Roadshow metrics you entered above.*")

if st.button("Calculate Final IPO Price (With Market Hype)"):
    final_valuation = base_valuation * calculated_hype
    ipo_price = final_valuation / shares_offered
    
    st.success(f"### 🎯 Final Predicted IPO Price for {company_name}: ${ipo_price:.2f} per share")
    
    st.write(f"**Investment Bank Breakdown:**")
    st.write(f"- 1. Base Intrinsic Valuation: **${base_valuation:,.2f} Million**")
    st.write(f"- 2. Valuation after **{calculated_hype:.2f}x** Roadshow Hype: **${final_valuation:,.2f} Million**")
    st.write(f"- 3. Divided by **{shares_offered} Million** shares = **${ipo_price:.2f} / share**")
    st.balloons()