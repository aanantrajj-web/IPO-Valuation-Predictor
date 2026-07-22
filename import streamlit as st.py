import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP ---
st.set_page_config(page_title="IPO Predictor Pro", layout="wide", initial_sidebar_state="collapsed")

# --- ROUTING LOGIC ---
# This reads the URL to see which page we should be on (defaults to 'home')
current_page = st.query_params.get("page", "home")

# --- CSS INJECTION (Header + App Styling) ---
st.markdown("""
    <style>
    /* HIDE DEFAULT STREAMLIT HEADER */
    [data-testid="stHeader"] { display: none; }
    
    /* PUSH MAIN CONTENT DOWN */
    .block-container { padding-top: 100px !important; max-width: 1000px; }

    /* TOP NAVIGATION HEADER CSS */
    .custom-header-wrapper {
        position: fixed; top: 0; left: 0; width: 100%; background-color: white;
        z-index: 999999; border-bottom: 1px solid #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .tier-1 { display: flex; justify-content: space-between; align-items: center; padding: 16px 32px; max-width: 1440px; margin: 0 auto; }
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

    /* MAIN APP BODY CSS */
    .stApp { background-color: #ffffff; background-image: linear-gradient(#f4f5f7 1px, transparent 1px), linear-gradient(90deg, #f4f5f7 1px, transparent 1px); background-size: 40px 40px; }
    label, p, .stMarkdown, li { color: #334155 !important; line-height: 1.6; }
    h1, h2, h3, h4 { color: #0f172a !important; }
    
    div.stButton > button:first-child { background-color: #3b82f6; color: white !important; font-weight: 600; border-radius: 30px; border: none; padding: 12px 30px; width: 100%; transition: all 0.2s ease; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2); }
    div.stButton > button:first-child:hover { background-color: #2563eb; transform: translateY(-2px); }
    div.stAlert { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { border-radius: 8px; border: 1px solid #cbd5e1; color: #0f172a !important; }
    
    /* Hero Section */
    .hero-title { font-size: 2.8rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.2rem; }
    .hero-italic { font-family: 'Georgia', serif; font-style: italic; color: #94a3b8 !important; }
    .hero-subtitle { color: #3b82f6 !important; font-size: 0.9rem; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- HTML INJECTION: DYNAMIC HEADER ---
# Notice how the hrefs are now "?page=home" and "?page=learn", and target="_self" prevents opening new tabs.
st.markdown(f"""
<div class="custom-header-wrapper">
    <div class="tier-1">
        <div class="nav-left">
            <a href="?page=home" class="brand-logo" target="_self">A.</a>
            <div class="nav-links">
                <a href="?page=home" target="_self" style="{ 'color: #0f172a; font-weight: 700;' if current_page == 'home' else '' }">
                    Explore <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 9l-7 7-7-7"></path></svg>
                </a>
                <a href="?page=learn" target="_self" style="{ 'color: #0f172a; font-weight: 700;' if current_page == 'learn' else '' }">
                    Learn <span class="badge-new">New</span>
                </a>
                <a href="#" target="_self">Investors</a>
                <a href="#" target="_self">Tools</a>
                <a href="#" target="_self">Market</a>
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
</div>
""", unsafe_allow_html=True)

# --- MACHINE LEARNING DATA SETUP ---
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
# PAGE ROUTING: HOME (CALCULATOR)
# ==========================================
if current_page == "home":
    st.markdown('<div class="hero-subtitle">AI VALUATION OPS • ONE WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Predict real-world IPOs<br>without getting lost in<br><span class="hero-italic">valuation chaos.</span></div>', unsafe_allow_html=True)
    st.write("") 

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
        st.info("This is the raw Total Company Value based *only* on our Machine Learning model analyzing core financials.")

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


# ==========================================
# PAGE ROUTING: LEARN (EDUCATIONAL HUB)
# ==========================================
elif current_page == "learn":
    st.markdown('<div class="hero-subtitle">INVESTOR EDUCATION HUB</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">The anatomy of an<br><span class="hero-italic">IPO valuation.</span></div>', unsafe_allow_html=True)
    st.write("Welcome to the methodology page. This guide equips investors and analysts with the financial knowledge required to understand how our predictive model translates raw data into market-ready valuations.")
    st.divider()
    
    st.markdown("### 1. The Quantitative Foundation (Machine Learning)")
    st.info("""
    **How the Model Learns:**
    This application is powered by a Scikit-Learn **Multiple Linear Regression** algorithm. 
    *   **Data Sourcing:** We started with historical IPO data managed in Excel and visualized in Power BI.
    *   **Algorithmic Weighting:** The algorithm evaluates three core financial inputs (Revenue, Margins, Cash Burn) against resulting historical valuations. It mathematically identifies the "weight" (importance) of each metric.
    *   **Predictive Pricing:** When you input a new company, the algorithm applies these historical weights to generate a pure, unbiased baseline valuation.
    """)
    
    st.markdown("### 2. Core Financial Fundamentals")
    st.write("""
    Before a company goes public, institutional investors assess intrinsic health using three primary pillars:
    *   **Revenue ($):** Represents total operational income. It validates product-market fit, scalability, and overall market demand. In our model, higher revenue applies a *positive multiplier* to the valuation.
    *   **Profit Margins (%):** The percentage of revenue retained as profit after expenses. It is a strict measure of operational efficiency and pricing power. 
    *   **Cash Burn ($):** The rate at which a company depletes its cash reserves before reaching profitability. High cash burn signals severe liquidity risk, triggering a *negative penalty* in the model's valuation.
    """)
    
    st.markdown("### 3. Share Dilution & Enterprise Value")
    st.write("""
    A common misconception for retail investors is equating "Share Price" directly to "Company Value." 
    *   **Enterprise Value:** The total intrinsic dollar value of the entire company (e.g., $10 Billion).
    *   **Share Price:** Simply the Enterprise Value divided by the arbitrary number of shares the Board of Directors decides to issue.
    
    Issuing 100 million shares prices the stock at $100. Issuing 1 billion shares prices it at $10. A lower share price does not mean the company is cheaper; it simply means the equity pie was sliced into smaller pieces.
    """)
    
    st.markdown("### 4. The Roadshow (Quantifying Market Hype)")
    st.write("""
    The public stock market is heavily influenced by macroeconomic trends and human psychology. Investment banks adjust their mathematical baseline through a process called the **Roadshow**.
    *   **Order Book Oversubscription:** If institutional demand exceeds the available share supply (e.g., 5x Oversubscribed), bankers possess leverage to command a price premium.
    *   **Macro Climate (S&P 500):** Bull markets provide a favorable environment for higher IPO pricing, whereas Bear markets force discounts.
    
    *Our tool automates this human element by calculating a mathematical **Hype Multiplier** based directly on inputted supply/demand ratios.*
    """)
