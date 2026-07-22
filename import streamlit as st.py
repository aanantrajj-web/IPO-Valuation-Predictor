import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP ---
st.set_page_config(page_title="IPO Predictor Pro", layout="wide", initial_sidebar_state="collapsed")

# --- CSS INJECTION (Header + App Styling) ---
st.markdown("""
    <style>
    /* 1. HIDE DEFAULT STREAMLIT HEADER */
    [data-testid="stHeader"] {
        display: none;
    }
    
    /* 2. PUSH MAIN CONTENT DOWN SO IT ISN'T HIDDEN BY THE FIXED HEADER */
    .block-container {
        padding-top: 150px !important;
        max-width: 1000px;
    }

    /* 3. TWO-TIER CUSTOM HEADER CSS */
    .custom-header-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 999999;
        border-bottom: 1px solid #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .tier-1 {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 32px;
        max-width: 1440px;
        margin: 0 auto;
    }
    .nav-left, .nav-right { display: flex; align-items: center; gap: 40px; }
    .brand-logo { font-size: 34px; font-weight: 900; color: #0f172a; text-decoration: none; letter-spacing: -2px; }
    .nav-links { display: flex; gap: 28px; }
    .nav-links a { text-decoration: none; color: #475569; font-weight: 500; font-size: 15px; display: flex; align-items: center; gap: 6px; transition: color 0.2s;}
    .nav-links a:hover { color: #0f172a; }
    .badge-new { background-color: #1e293b; color: white; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 999px; text-transform: uppercase; margin-left: 2px;}
    .search-container { position: relative; width: 350px; }
    .search-input { width: 100%; background: #f1f5f9; border: 2px solid transparent; border-radius: 999px; padding: 10px 16px 10px 40px; font-size: 14px; outline: none; transition: 0.2s; color: #0f172a;}
    .search-input:focus { background: white; border-color: #3b82f6; }
    .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
    .login-btn { text-decoration: none; color: #334155; font-weight: 600; font-size: 15px; transition: color 0.2s; }
    .login-btn:hover { color: #0f172a; }

    .tier-2 {
        display: flex;
        gap: 12px;
        padding: 12px 32px;
        max-width: 1440px;
        margin: 0 auto;
        border-top: 1px solid #f1f5f9;
        overflow-x: auto;
    }
    .filter-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #334155;
        cursor: pointer;
        white-space: nowrap;
        transition: background 0.2s;
    }
    .filter-btn:hover { background: #f1f5f9; }
    .chevron-icon { width: 14px; height: 14px; stroke: currentColor; stroke-width: 2; fill: none; }

    /* 4. MAIN APP BODY CSS */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(#f4f5f7 1px, transparent 1px), linear-gradient(90deg, #f4f5f7 1px, transparent 1px);
        background-size: 40px 40px;
    }
    label, p, .stMarkdown, li { color: #334155 !important; }
    h1, h2, h3, h4 { color: #0f172a !important; }

    div.stButton > button:first-child {
        background-color: #3b82f6; color: white !important; font-weight: 600; border-radius: 30px; border: none; padding: 12px 30px; width: 100%; transition: all 0.2s ease; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
    }
    div.stButton > button:first-child:hover { background-color: #2563eb; transform: translateY(-2px); }
    div.stAlert { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { border-radius: 8px; border: 1px solid #cbd5e1; color: #0f172a !important; }
    
    /* Hero Section */
    .hero-title { font-size: 2.8rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.2rem; }
    .hero-italic { font-family: 'Georgia', serif; font-style: italic; color: #94a3b8 !important; }
    .hero-subtitle { color: #3b82f6 !important; font-size: 0.9rem; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 1rem; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border-radius: 4px 4px 0px 0px; padding-top: 10px; padding-bottom: 10px; color: #64748b; font-weight: 600; font-size: 1.1rem; }
    .stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom-color: #3b82f6 !important; }
    </style>
""", unsafe_allow_html=True)


# --- HTML INJECTION: THE TWO-TIER HEADER ---
st.markdown("""
<div class="custom-header-wrapper">
    <!-- TIER 1: MAIN NAVIGATION -->
    <div class="tier-1">
        <div class="nav-left">
            <a href="#" class="brand-logo">A.</a>
            <div class="nav-links">
                <a href="#">Explore <svg class="chevron-icon" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg></a>
                <a href="#">Learn <span class="badge-new">New</span></a>
                <a href="#">Investors</a>
                <a href="#">Tools</a>
                <a href="#">Market</a>
            </div>
        </div>
        <div class="nav-right">
            <div class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" placeholder="Search by companies, metrics..." />
            </div>
            <a href="#" class="login-btn">Log in</a>
        </div>
    </div>
    
    <!-- TIER 2: FILTER PILLS -->
    <div class="tier-2">
        <button class="filter-btn">Valuation Range <svg class="chevron-icon" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg></button>
        <button class="filter-btn">Sector <svg class="chevron-icon" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg></button>
        <button class="filter-btn">Market Sentiment <svg class="chevron-icon" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg></button>
        <button class="filter-btn">Country <svg class="chevron-icon" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg></button>
    </div>
</div>
""", unsafe_allow_html=True)


# --- MAIN APP CONTENT ---
st.markdown('<div class="hero-subtitle">AI VALUATION OPS • ONE WORKSPACE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Predict real-world IPOs<br>without getting lost in<br><span class="hero-italic">valuation chaos.</span></div>', unsafe_allow_html=True)
st.write("") 

# Tabs
tab1, tab2 = st.tabs(["📊 Calculations", "📚 Learn"])

# --- MACHINE LEARNING MODEL SETUP ---
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

    st.header("Phase 2: Share Dilution")
    shares_offered = st.number_input("Total Shares Issued to Public (in millions)", value=150.0)

    if st.button("Calculate Base IPO Price (No Hype)"):
        base_ipo_price = base_valuation / shares_offered
        st.success(f"### 📈 Base IPO Price: ${base_ipo_price:.2f} per share")

    st.divider()

    st.header("Phase 3: The Roadshow (Supply & Demand)")
    col_a, col_b = st.columns(2)
    with col_a:
        shares_demanded = st.number_input("Total Shares Demanded by Investors ($M)", value=450.0)
    with col_b:
        sp500_return = st.number_input("S&P 500 YTD Return (%)", value=12.0)

    oversubscription = max(shares_demanded / shares_offered, 0.1) 
    oversub_mod = (oversubscription - 1.0) * 0.05 
    climate_mod = 0.15 if sp500_return >= 10 else (-0.15 if sp500_return <= 0 else 0.0)

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
