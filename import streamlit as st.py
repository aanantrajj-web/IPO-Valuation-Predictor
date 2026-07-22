import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. Set up the Website Design
st.set_page_config(page_title="IPO Predictor", layout="centered")
st.title("📈 IPO Valuation Predictor")
st.write("Enter a company's financial metrics below to instantly predict its base IPO price using Machine Learning.")

# 2. Create the Input Forms for the User
company_name = st.text_input("Company Name", "e.g., SpaceX")
revenue_growth = st.number_input("Revenue Growth (%)", value=15.0)
ebitda = st.number_input("EBITDA (in millions)", value=5.0)
readiness_score = st.slider("Market Readiness Score", 0.0, 100.0, 62.5)

# 3. Dummy Training Data (You would normally load your Excel file here)
# For the easiest web version, we train a quick model on the fly
data = {
    'Revenue Growth': [10, 20, 5, 30, 15],
    'EBITDA': [2, 8, -1, 15, 5],
    'Readiness Score': [40, 70, 20, 90, 62],
    'Final Price': [15, 35, 10, 50, 28]
}
df = pd.DataFrame(data)

# Train the Model
X = df[['Revenue Growth', 'EBITDA', 'Readiness Score']]
y = df['Final Price']
model = LinearRegression()
model.fit(X, y)

# 4. The Calculate Button
if st.button("Calculate Predicted IPO Price"):
    # Run the prediction
    input_data = pd.DataFrame([[revenue_growth, ebitda, readiness_score]], 
                              columns=['Revenue Growth', 'EBITDA', 'Readiness Score'])
    prediction = model.predict(input_data)[0]
    
    # Display the result
    st.success(f"### Predicted IPO Price for {company_name}: ${prediction:.2f}")
    st.balloons()