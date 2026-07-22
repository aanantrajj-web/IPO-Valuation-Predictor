import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Set up the Website Design
st.set_page_config(page_title="IPO Predictor", layout="centered")
st.title("📈 Real-World IPO Valuation Predictor")
st.write("Enter financial metrics, share count, and market sentiment to calculate a real-world IPO price.")

# 2. Real Inputs matching your Excel file
st.markdown("### 📊 1. Core Financial Fundamentals")
company_name = st.text_input("Company Name", "e.g., Reddit")
revenue = st.number_input("Revenue (in millions)", value=804.0)
profit_margin = st.number_input("Profit Margins (%)", value=-11.0)
cash_burn = st.number_input("Cash Burn", value=90.0)

# Automatically Calculate Market Readiness Score
calculated_readiness = min(max(50 + (profit_margin * 2) + (revenue / 1000) - (cash_burn / 10), 0), 100)
st.info(f"**Calculated Market Readiness Score:** {calculated_readiness:.2f} / 100")

# 3. New Real-World Mechanics (Shares & Marketing Hype)
st.markdown("### 🏦 2. Real-World IPO Mechanics")
shares_offered = st.number_input("Total Shares Issued (in millions)", value=150.0)
market_sentiment = st.slider("Roadshow Hype Premium (1.0 = Neutral)", 0.5, 2.0, 1.2)
st.caption("Slide right for high brand demand (oversubscribed), slide left for cold market.")

# 4. Training Data (Now predicting TOTAL VALUATION instead of share price)
data = {
    'Revenue': [3000, 25000, 250, 20000, 500, 804],
    'Profit Margins': [12, 15, -40, 8, -20, -11],
    'Cash Burn': [0, 0, 100, 0, 150, 90],
    'Total Valuation': [15000, 125000, 1200, 80000, 2500, 5500] 
}
df = pd.DataFrame(data)

# Train the Model on Total Valuation
X = df[['Revenue', 'Profit Margins', 'Cash Burn']]
y = df['Total Valuation']
model = LinearRegression()
model.fit(X, y)

# 5. The Calculate Button
if st.button("Calculate Real-World IPO Price"):
    # Predict Total Base Valuation using Machine Learning
    input_data = pd.DataFrame([[revenue, profit_margin, cash_burn]], 
                              columns=['Revenue', 'Profit Margins', 'Cash Burn'])
    
    # Ensure valuation doesn't drop below a minimum threshold
    base_valuation = max(model.predict(input_data)[0], 100) 
    
    # Apply the Roadshow Hype Premium
    final_valuation = base_valuation * market_sentiment
    
    # The Real-World Math: Divide Valuation by Shares
    ipo_price = final_valuation / shares_offered
    
    # Display the result
    st.success(f"### Predicted IPO Price for {company_name}: ${ipo_price:.2f} per share")
    
    # Show the "Under the Hood" Math to the recruiter
    st.write(f"**Under the hood math:**")
    st.write(f"- Base Intrinsic Valuation: **${base_valuation:,.2f} Million**")
    st.write(f"- Valuation after {market_sentiment}x Market Hype: **${final_valuation:,.2f} Million**")
    st.write(f"- Divided by {shares_offered} Million shares = **${ipo_price:.2f} / share**")
    st.balloons()