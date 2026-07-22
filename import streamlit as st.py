import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP & HIREZAPP-STYLE CSS ---
st.set_page_config(page_title="IPO Predictor Pro", layout="centered")

st.markdown("""
    <style>
    /* 1. Subtle Geometric Grid Background */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(#f4f5f7 1px, transparent 1px), linear-gradient(90deg, #f4f5f7 1px, transparent 1px);
        background-size: 40px 40px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. Vibrant Blue Pill-Shaped Buttons */
    div.stButton > button:first-child {
        background-color: #3b82f6; /* Modern SaaS Blue */
        color: white;
        font-weight: 600;
        border-radius: 30px; /* Pill shape */
        border: none;
        padding: 12px 30px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        width: 100%;
    }

    /* Button Hover Effect */
    div.stButton > button:first-child:hover {
        background-color: #2563eb;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.4);
    }

    /* 3. Clean White Info Cards */
    div.stAlert {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        color: #334155;
    }
    
    /* 4. Sleek Input Fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
    }

    /* Hero Text Styling */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }
    .hero-italic {
        font-family: 'Georgia', serif;
        font-style: italic;
        color: #94a3b8;
        font-weight: normal;
    }
    .hero-subtitle {
        color: #3b82f6;
        font-size: 0.9rem;
        letter-spacing: 1.5px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CUSTOM HERO HEADER (Mimicking the Screenshot) ---
st.markdown('<div class="hero-subtitle">AI VALUATION OPS • ONE WORKSPACE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Predict real-world IPOs<br>without getting lost in<br><span class="hero-italic">valuation chaos.</span></div>', unsafe_allow_html=True)
st.write("") # Spacer

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
st.header("Phase 2: Share Dilution")
shares_offered = st.number_input("Total Shares Issued to Public (in millions)", value=150.0)

if st.button("Calculate Base IPO Price (No Hype)"):
    base_ipo_price = base_valuation / shares_offered
    st.success(f"### 📈 Base IPO Price: ${base_ipo_price:.2f} per share")

st.divider()

# --- SECTION 3: REAL-WORLD MECHANICS (QUANTIFIED ROADSHOW) ---
st.header("Phase 3: The Roadshow (Supply & Demand)")
st.markdown("""
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
oversubscription = max(shares_demanded / shares_offered, 0.1) 
oversub_mod = (oversubscription - 1.0) * 0.05 
climate_mod = 0.15 if sp500_return >= 10 else (-0.15 if sp500_return <= 0 else 0.0)

# Calculate final automatic hype
calculated_hype = 1.0 + oversub_mod + climate_mod
calculated_hype = max(min(calculated_hype, 2.5), 0.5) 

# --- THE AUTOMATIC BAR ---
st.write("### 📊 Automated Market Sentiment Bar")
st.slider("Calculated Hype Premium (1.0 = Neutral)", 0.5, 2.5, float(calculated_hype), disabled=True)

if st.button("Calculate Final IPO Price (With Market Hype)"):
    final_valuation = base_valuation * calculated_hype
    ipo_price = final_valuation / shares_offered
    
    st.success(f"### 🎯 Final Predicted IPO Price for {company_name}: ${ipo_price:.2f} per share")
    
    st.write(f"**Investment Bank Breakdown:**")
    st.write(f"- 1. Base Intrinsic Valuation: **${base_valuation:,.2f} Million**")
    st.write(f"- 2. Valuation after **{calculated_hype:.2f}x** Roadshow Hype: **${final_valuation:,.2f} Million**")
    st.write(f"- 3. Divided by **{shares_offered} Million** shares = **${ipo_price:.2f} / share**")
    st.balloons()
