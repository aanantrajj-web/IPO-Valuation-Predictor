import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP ---
st.set_page_config(page_title="IPO Predictor Pro", layout="wide", initial_sidebar_state="collapsed")

# --- ROUTING LOGIC ---
current_page = st.query_params.get("page", "home")

# --- CSS INJECTION (Header, Full-Width Ticker, & App Styling) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none; }
    
    /* Ensure main container leaves room for bottom ticker */
    .block-container { 
        padding-top: 100px !important; 
        padding-bottom: 90px !important; 
        max-width: 1000px; 
    }
    
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

    /* BOTTOM FULL-WIDTH FLOATING STOCK TICKER CSS */
    .stock-ticker-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background-color: #0f172a;
        color: white;
        overflow: hidden;
        white-space: nowrap;
        z-index: 999999;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        padding: 12px 0;
        border-top: 1px solid #334155;
        box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.2);
        margin: 0;
    }
    .stock-ticker-track {
        display: inline-block;
        white-space: nowrap;
        animation: marquee 35s linear infinite;
    }
    .stock-ticker-track:hover {
        animation-play-state: paused;
    }
    @keyframes marquee {
        0% { transform: translateX(0%); }
        100% { transform: translateX(-50%); }
    }
    .stock-item {
        display: inline-block;
        margin-right: 40px;
    }
    .stock-name { font-weight: 700; color: #94a3b8; letter-spacing: 0.5px; }
    .stock-price { margin-left: 6px; font-weight: 600; color: #f8fafc; }
    .stock-up { color: #4ade80; margin-left: 6px; font-weight: 600; }
    .stock-down { color: #f87171; margin-left: 6px; font-weight: 600; }

    /* MAIN APP BODY CSS */
    .stApp { background-color: #ffffff; background-image: linear-gradient(#f4f5f7 1px, transparent 1px), linear-gradient(90deg, #f4f5f7 1px, transparent 1px); background-size: 40px 40px; }
    label, p, .stMarkdown, li { color: #334155 !important; line-height: 1.6; }
    h1, h2, h3, h4 { color: #0f172a !important; }
    div.stButton > button:first-child { background-color: #3b82f6; color: white !important; font-weight: 600; border-radius: 30px; border: none; padding: 12px 30px; width: 100%; transition: all 0.2s ease; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2); }
    div.stButton > button:first-child:hover { background-color: #2563eb; transform: translateY(-2px); }
    div.stAlert { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { border-radius: 8px; border: 1px solid #cbd5e1; color: #0f172a !important; }
    .hero-title { font-size: 2.8rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.2rem; }
    .hero-italic { font-family: 'Georgia', serif; font-style: italic; color: #94a3b8 !important; }
    .hero-subtitle { color: #3b82f6 !important; font-size: 0.9rem; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- HTML INJECTION: TOP NAVIGATION HEADER ---
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

# --- HTML INJECTION: FULL-WIDTH BOTTOM FLOATING STOCK TICKER ---
st.markdown("""
<div class="stock-ticker-wrapper">
    <div class="stock-ticker-track">
        <span class="stock-item"><span class="stock-name">NIFTY 50</span><span class="stock-price">23,458.20</span><span class="stock-up">+145.30 (+0.62%)</span></span>
        <span class="stock-item"><span class="stock-name">NIFTY BANK</span><span class="stock-price">50,120.50</span><span class="stock-up">+320.10 (+0.64%)</span></span>
        <span class="stock-item"><span class="stock-name">RELIANCE</span><span class="stock-price">₹2,980.15</span><span class="stock-up">+24.50 (+0.83%)</span></span>
        <span class="stock-item"><span class="stock-name">TCS</span><span class="stock-price">₹4,120.00</span><span class="stock-down">-12.30 (-0.30%)</span></span>
        <span class="stock-item"><span class="stock-name">HDFC BANK</span><span class="stock-price">₹1,540.80</span><span class="stock-up">+8.40 (+0.55%)</span></span>
        <span class="stock-item"><span class="stock-name">INFOSYS</span><span class="stock-price">₹1,650.25</span><span class="stock-down">-5.10 (-0.31%)</span></span>
        <span class="stock-item"><span class="stock-name">ICICI BANK</span><span class="stock-price">₹1,115.40</span><span class="stock-up">+14.20 (+1.29%)</span></span>
        <span class="stock-item"><span class="stock-name">ITC</span><span class="stock-price">₹435.60</span><span class="stock-up">+2.10 (+0.48%)</span></span>
        <span class="stock-item"><span class="stock-name">SBIN</span><span class="stock-price">₹820.50</span><span class="stock-down">-4.80 (-0.58%)</span></span>
        <span class="stock-item"><span class="stock-name">BHARTI AIRTEL</span><span class="stock-price">₹1,410.90</span><span class="stock-up">+18.30 (+1.31%)</span></span>
        <span class="stock-item"><span class="stock-name">L&T</span><span class="stock-price">₹3,560.00</span><span class="stock-up">+42.10 (+1.19%)</span></span>
        <span class="stock-item"><span class="stock-name">HINDUNILVR</span><span class="stock-price">₹2,450.10</span><span class="stock-down">-6.20 (-0.25%)</span></span>
        
        <!-- DUPLICATE SET FOR SMOOTH INFINITE LOOP -->
        <span class="stock-item"><span class="stock-name">NIFTY 50</span><span class="stock-price">23,458.20</span><span class="stock-up">+145.30 (+0.62%)</span></span>
        <span class="stock-item"><span class="stock-name">NIFTY BANK</span><span class="stock-price">50,120.50</span><span class="stock-up">+320.10 (+0.64%)</span></span>
        <span class="stock-item"><span class="stock-name">RELIANCE</span><span class="stock-price">₹2,980.15</span><span class="stock-up">+24.50 (+0.83%)</span></span>
        <span class="stock-item"><span class="stock-name">TCS</span><span class="stock-price">₹4,120.00</span><span class="stock-down">-12.30 (-0.30%)</span></span>
        <span class="stock-item"><span class="stock-name">HDFC BANK</span><span class="stock-price">₹1,540.80</span><span class="stock-up">+8.40 (+0.55%)</span></span>
        <span class="stock-item"><span class="stock-name">INFOSYS</span><span class="stock-price">₹1,650.25</span><span class="stock-down">-5.10 (-0.31%)</span></span>
        <span class="stock-item"><span class="stock-name">ICICI BANK</span><span class="stock-price">₹1,115.40</span><span class="stock-up">+14.20 (+1.29%)</span></span>
        <span class="stock-item"><span class="stock-name">ITC</span><span class="stock-price">₹435.60</span><span class="stock-up">+2.10 (+0.48%)</span></span>
        <span class="stock-item"><span class="stock-name">SBIN</span><span class="stock-price">₹820.50</span><span class="stock-down">-4.80 (-0.58%)</span></span>
        <span class="stock-item"><span class="stock-name">BHARTI AIRTEL</span><span class="stock-price">₹1,410.90</span><span class="stock-up">+18.30 (+1.31%)</span></span>
        <span class="stock-item"><span class="stock-name">L&T</span><span class="stock-price">₹3,560.00</span><span class="stock-up">+42.10 (+1.19%)</span></span>
        <span class="stock-item"><span class="stock-name">HINDUNILVR</span><span class="stock-price">₹2,450.10</span><span class="stock-down">-6.20 (-0.25%)</span></span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PAGE ROUTING: HOME (CALCULATOR)
# ==========================================
if current_page == "home":
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
# PAGE ROUTING: LEARN
# ==========================================
elif current_page == "learn":
    learn_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        background-color: #ffffff;
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        color: #1a202c;
        margin: 0;
        padding: 20px;
    }
    .article-container {
        max-width: 1000px;
        margin: 0 auto;
        padding-bottom: 60px;
    }
    .breadcrumb { color: #007b8a; font-weight: 600; font-size: 13px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
    .article-hr { border: 0; border-top: 1px solid #e2e8f0; margin-bottom: 30px; }
    .article-title { color: #2c3e50; font-size: 38px; font-weight: 700; margin-bottom: 24px; line-height: 1.2; }
    .article-intro { font-size: 16px; line-height: 1.6; margin-bottom: 24px; color: #2d3748; }
    .toc-list { margin: 0 0 40px 0; padding-left: 20px; }
    .toc-list li { margin-bottom: 8px; font-size: 16px; }
    .teal-link { color: #007b8a; text-decoration: none; font-weight: 500; }
    .teal-link:hover { text-decoration: underline; }
    .section-title { font-size: 22px; font-weight: 700; margin-top: 40px; margin-bottom: 15px; color: #0f172a; }
    .article-text { font-size: 16px; line-height: 1.7; margin-bottom: 20px; color: #1a202c; }

    .featured-section-title { font-size: 28px; font-weight: 700; color: #0b2239; margin-top: 60px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
    .featured-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 20px; }
    .featured-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column; }
    .card-banner { height: 130px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #e2e8f0; padding: 10px; }
    .banner-1 { background-color: #f7f5f0; }
    .banner-2 { background-color: #ffffff; }
    .banner-3 { background-color: #ffffff; }
    .banner-4 { background-color: #e57373; }
    .card-body { padding: 18px; display: flex; flex-direction: column; flex-grow: 1; }
    .card-title { font-size: 18px; font-weight: 700; color: #003366; margin-bottom: 12px; line-height: 1.3; }
    .card-desc { font-size: 14px; color: #333333; line-height: 1.5; }
    </style>
    </head>
    <body>
    <div class="article-container">
        <div class="breadcrumb">HOME</div>
        <hr class="article-hr">
        <div class="article-title">Introduction to Investing</div>
        <div class="article-intro">
            Through investing, you can build wealth for a strong financial future. Defining your goals and creating and sticking to a plan by regularly setting money aside for investments can drive life-changing results over time.
        </div>
        <ul class="toc-list">
            <li><a href="#" class="teal-link">What is Investing?</a></li>
            <li><a href="#" class="teal-link">Compound Growth</a></li>
            <li><a href="#" class="teal-link">Managing Risk</a></li>
            <li><a href="#" class="teal-link">Asset Allocation and Diversification</a></li>
            <li><a href="#" class="teal-link">Long-Term Investments</a></li>
            <li><a href="#" class="teal-link">Savings and Short-Term Investments</a></li>
            <li><a href="#" class="teal-link">Investing for Your Children</a></li>
            <li><a href="#" class="teal-link">Other Steps to Build Wealth Over Time</a></li>
        </ul>
        <div class="section-title">What is Investing?</div>
        <div class="article-text">
            Both saving and investing mean you're setting aside some of the money you earn, separate from what you spend on needs and wants. A savings account is a good choice for short-term goals or to hold an emergency fund that can cover unexpected expenses.
        </div>
        <div class="featured-section-title">Featured Content</div>
        <div class="featured-grid">
            <div class="featured-card">
                <div class="card-banner banner-1"><div style="text-align: center; font-weight: bold; font-family: serif; font-size: 20px;">Trump Accounts</div></div>
                <div class="card-body"><div class="card-title">Jumpstart Your Child's Future</div><div class="card-desc">Learn how to enroll in accounts today!</div></div>
            </div>
            <div class="featured-card">
                <div class="card-banner banner-2"><div style="text-align: center; font-weight: bold; color: #002868;">NIFTY & SENSEX</div></div>
                <div class="card-body"><div class="card-title">Market Analysis</div><div class="card-desc">Track real-time index performances and economic indicators.</div></div>
            </div>
            <div class="featured-card">
                <div class="card-banner banner-3"><div style="font-size: 30px; color: #002868; font-weight: bold;">☑ ✔</div></div>
                <div class="card-body"><div class="card-title">Tax-Advantaged Accounts</div><div class="card-desc">Learn how to maximize tax benefits on investments.</div></div>
            </div>
            <div class="featured-card">
                <div class="card-banner banner-4"><div style="font-size: 36px; color: white;">📈</div></div>
                <div class="card-body"><div class="card-title">Financial Calculators</div><div class="card-desc">Access compound interest and valuation tools.</div></div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """
    st.components.v1.html(learn_html, height=1200, scrolling=True)
