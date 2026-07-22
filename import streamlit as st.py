import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Set up the Website Design
st.set_page_config(page_title="IPO Predictor", layout="centered")
st.title("📈 IPO Valuation Predictor")
st.write("Enter a company's financial metrics below to calculate its Market Readiness and predict its base IPO price.")

# 2. Real Inputs matching your Excel file
company_name = st.text_input("Company Name", "e.g., SpaceX")
revenue = st.number_input("Revenue (in millions)", value=8500.0)
profit_margin = st.number_input("Profit Margins (%)", value=5.0)
cash_burn = st.number_input("Cash Burn", value=0.0)

# 3. Automatically Calculate Market Readiness Score (Out of 100)
# Logic: Baseline of 50, add points for profit/revenue, subtract for cash burn.
calculated_readiness = min(max(50 + (profit_margin * 2) + (revenue / 1000) - (cash_burn / 10), 0), 100)

st.info(f"📊 **Calculated Market Readiness Score:** {calculated_readiness:.2f} / 100")

# 4. Dummy Training Data (Matches your actual columns now)
data = {
    'Revenue': [3000, 25000, 250, 20000, 500],
    'Profit Margins': [12, 15, -40, 8, -20],
    'Cash Burn': [0, 0, 100, 0, 150],
    'Final Price': [35, 45, 12, 40, 15]
}
df = pd.DataFrame(data)

# Train the Model on the 3 real metrics
X = df[['Revenue', 'Profit Margins', 'Cash Burn']]
y = df['Final Price']
model = LinearRegression()
model.fit(X, y)

# 5. The Calculate Button
if st.button("Calculate Predicted IPO Price"):
    # Run the prediction using the exact columns
    input_data = pd.DataFrame([[revenue, profit_margin, cash_burn]], 
                              columns=['Revenue', 'Profit Margins', 'Cash Burn'])
    prediction = model.predict(input_data)[0]
    
    # Display the result
    st.success(f"### Predicted IPO Price for {company_name}: ${prediction:.2f}")
    st.balloons()