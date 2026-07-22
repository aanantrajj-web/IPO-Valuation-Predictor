import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP & HIREZAPP-STYLE CSS ---
st.set_page_config(page_title="IPO Predictor Pro", layout="centered")

st.markdown("""
    <style>
    /* Background and Fonts */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(#f4f5f7 1px, transparent 1px), linear-gradient(90deg, #f4f5f7 1px, transparent 1px);
        background-size: 40px 40px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Force Text Colors */
    label, p, .stMarkdown, div[data-testid="stMarkdownContainer"], li {
        color: #334155 !important; 
    }
    h1, h2, h3, h4 {
        color: #0f172a !important;
    }

    /* Vibrant Blue Pill Buttons */
    div.stButton > button:first-child {
        background-color: #3b82f6; 
        color: white !important;
        font-weight: 600;
        border-radius: 30px; 
        border: none;
        padding: 12px 30px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }

    /* Style Info Cards & Inputs */
    div.stAlert {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        color: #334155 !important;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        color: #0f172a !important;
    }
    
    /* Style Tabs to look like a clean Nav Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #64748b;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom-color: #3b82f6 !important;
    }

    /* Hero Text */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }
    .hero-italic {
        font-family: 'Georgia', serif;
        font-style: italic;
        color: #94a3b8 !important;
    }
    .hero-subtitle {
        color: #3b82f6 !important;
        font-size: 0.9rem;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CUSTOM HERO HEADER ---
st.markdown('<div class="hero-subtitle">AI VALUATION OPS • ONE WORKSPACE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Predict real-world IPOs<br>without getting lost in<br><span class="hero-italic">valuation chaos.</span></div>', unsafe_allow_html=True)
st.write("") # Spacer

# --- CREATE THE NAVIGATION TABS ---
tab1, tab2 = st.tabs(["📊 Calculations", "📚 Learn"])

# --- MACHINE LEARNING MODEL SETUP (Runs for both tabs) ---
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


# ==========================================
# TAB 1: THE CALCULATOR
# ==========================================
with tab1:
    st.header("Phase 1: Intrinsic Financial Fundamentals")
    
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
        st.info("This is the raw Total Company Value based *only* on our Machine Learning model analyzing core financials. It ignores market hype and share dilution.")

    st.divider() 

    # --- Phase 2: Shares ---
    st.header("Phase 2: Share Dilution")
    shares_offered = st.number_input("Total Shares Issued to Public (in millions)", value=150.0)

    if st.button("Calculate Base IPO Price (No Hype)"):
        base_ipo_price = base_valuation / shares_offered
        st.success(f"### 📈 Base IPO Price: ${base_ipo_price:.2f} per share")
        st.info(f"Math: **${base_valuation:,.2f}M** Total Value ÷ **{shares_offered}M** Shares.")

    st.divider()

    # --- Phase 3: Roadshow ---
    st.header("Phase 3: The Roadshow (Supply & Demand)")
    st.markdown("*Enter real-world market metrics below. The **Roadshow Premium Bar** will automatically calculate the hype multiplier.*")

    col_a, col_b = st.columns(2)
    with col_a:
        shares_demanded = st.number_input("Total Shares Demanded by Investors ($M)", value=450.0)
    with col_b:
        sp500_return = st.number_input("S&P 500 YTD Return (%)", value=12.0)

    # The Math that drives the automatic bar
    oversubscription = max(shares_demanded / shares_offered, 0.1) 
    oversub_mod = (oversubscription - 1.0) * 0.05 
    climate_mod = 0.15 if sp500_return >= 10 else (-0.15 if sp500_return <= 0 else 0.0)

    # Calculate final automatic hype
    calculated_hype = 1.0 + oversub_mod + climate_mod
    calculated_hype = max(min(calculated_hype, 2.5), 0.5) 

    st.write("### 📊 Automated Market Sentiment Bar")
    st.slider("Calculated Hype Premium (1.0 = Neutral)", 0.5, 2.5, float(calculated_hype), disabled=True)

    if st.button("Calculate Final IPO Price (With Market Hype)"):
        final_valuation = base_valuation * calculated_hype
        ipo_price = final_valuation / shares_offered
        
        st.success(f"### 🎯 Final Predicted IPO Price for {company_name}: ${ipo_price:.2f} per share")
        
        st.write(f"**Investment Bank Breakdown:**")
        st.write(f"- 1. Base ML Valuation: **${base_valuation:,.2f} Million**")
        st.write(f"- 2. Valuation after **{calculated_hype:.2f}x** Roadshow Hype: **${final_valuation:,.2f} Million**")
        st.write(f"- 3. Divided by **{shares_offered} Million** shares = **${ipo_price:.2f} / share**")
        st.balloons()


# ==========================================
# TAB 2: THE LEARNING CENTER
# ==========================================
with tab2:
    st.header("📚 The Educational Hub")
    st.write("Welcome to the methodology page. Here is a full breakdown of how this tool turns raw Excel data into a live, institutional-grade pricing model.")
    
    st.markdown("### 1. The Data Pipeline (From Excel to Web)")
    st.info("""
    **How the Model Learns:**
    This app is powered by a Scikit-Learn **Multiple Linear Regression** algorithm. 
    1. We started with historical IPO data managed in **Excel** and visualized in **Power BI**.
    2. We extracted the core financial inputs (Revenue, Profit Margin, Cash Burn) and the resulting Total Valuation.
    3. The algorithm reads this historical data and assigns mathematical "weights" to each metric. 
    4. When you enter new data on the 'Calculations' tab, the algorithm uses those historical weights to predict a brand new, unseen company's valuation.
    """)
    
    st.markdown("### 2. The Core Financial Metrics")
    st.write("""
    Before a company goes public, investment bankers assess its intrinsic health using these three pillars:
    *   **Revenue:** The total amount of money brought in by operations. It proves scale and market demand. (Positive weight in our model).
    *   **Profit Margins:** The percentage of revenue that remains as profit. It proves operational efficiency. (Highly positive weight in our model).
    *   **Cash Burn:** The rate at which a company spends its cash reserves, usually before generating positive cash flow. (Negative weight in our model, as it implies high risk).
    """)
    
    st.markdown("### 3. Share Dilution")
    st.write("""
    A Total Company Valuation is largely theoretical until you cut the company into individual shares for the public to buy. 
    If our Machine Learning model values a company at $10 Billion:
    *   Issuing 100 Million shares = $100 per share.
    *   Issuing 1 Billion shares = $10 per share. 
    
    This is why a lower share price doesn't necessarily mean a "cheaper" or worse company; it just means the equity pie was cut into more pieces.
    """)
    
    st.markdown("### 4. The Roadshow & Market Hype")
    st.write("""
    The stock market is not perfectly rational; it is driven by human emotion and macroeconomic trends. 
    After bankers set a baseline price, they go on a **"Roadshow"** to pitch the company to institutional investors. 
    *   **Oversubscription:** If investors demand more shares than are actually available, the bank raises the price.
    *   **Macro Climate:** If the broader stock market (like the S&P 500) is performing exceptionally well, investors are willing to pay a premium. 
    
    *Our model quantifies this human emotion by calculating a **Hype Multiplier** based on actual supply/demand ratios and S&P 500 returns.*
    """)
