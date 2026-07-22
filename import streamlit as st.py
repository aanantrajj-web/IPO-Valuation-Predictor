import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- SETUP ---
st.set_page_config(page_title="IPO Predictor Pro", layout="wide", initial_sidebar_state="collapsed")

# --- ROUTING LOGIC ---
current_page = st.query_params.get("page", "home")

# --- CSS INJECTION (Header + App Styling) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none; }
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
    .hero-title { font-size: 2.8rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.2rem; }
    .hero-italic { font-family: 'Georgia', serif; font-style: italic; color: #94a3b8 !important; }
    .hero-subtitle { color: #3b82f6 !important; font-size: 0.9rem; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- HTML INJECTION: DYNAMIC HEADER ---
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


# ==========================================
# PAGE ROUTING: HOME (CALCULATOR)
# ==========================================
if current_page == "home":
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
# PAGE ROUTING: LEARN (CUSTOM ARTICLE UI)
# ==========================================
elif current_page == "learn":
    # HTML must NOT be indented here, otherwise Streamlit renders it as a code block
    st.markdown("""
<style>
.article-container {
    max-width: 900px;
    margin: 0 auto;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    color: #1a202c;
    padding-bottom: 100px;
}
.breadcrumb {
    color: #007b8a;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.article-hr {
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin-bottom: 30px;
}
.article-title {
    color: #5a6b7c;
    font-size: 38px;
    font-weight: 600;
    margin-bottom: 24px;
    line-height: 1.2;
}
.article-intro {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 24px;
    color: #2d3748;
}
.toc-list {
    margin: 0 0 35px 0;
    padding-left: 20px;
}
.toc-list li {
    margin-bottom: 6px;
    font-size: 16px;
}
.teal-link {
    color: #007b8a;
    text-decoration: none;
    font-weight: 400;
}
.teal-link:hover {
    text-decoration: underline;
}
.section-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 15px;
    color: #0f172a;
}
.article-text {
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 20px;
    color: #1a202c;
}
</style>

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
        Both saving and investing mean you're setting aside some of the money you earn, separate from what you spend on needs and wants. A savings account is a good choice for short-term goals or to hold an emergency fund that can cover unexpected expenses. You can open a savings account at a <a href="#" class="teal-link">bank</a> or <a href="#" class="teal-link">credit union</a>, and the money you deposit there is typically federally insured. Most banks or credit unions will pay some interest on your savings.
    </div>
    <div class="article-text">
        Investing is when you put your money into assets such as <a href="#" class="teal-link">stocks</a> or <a href="#" class="teal-link">bonds</a>, often held in a brokerage or advisory account, with the expectation of making a return over time. Return from an asset may come from an increase in the asset's value or from an asset's interest or <a href="#" class="teal-link">dividend</a> payments to those who own it.
    </div>

    <div class="section-title">Compound Growth</div>
    <div class="article-text">
        Compound growth, or compounding, is the mathematical process by which an asset's earnings are reinvested to generate their own earnings over time. This concept applies equally to traditional savings accounts and broader investment portfolios. When you utilize <a href="#" class="teal-link">compound interest</a>, you are essentially making your money work for you, creating a snowball effect that accelerates the growth of your wealth.
    </div>

    <div class="section-title">Managing Risk</div>
    <div class="article-text">
        All investments carry some degree of risk. Unlike a standard bank account, money invested in the stock market is not guaranteed to grow, and you could lose the principal amount you started with. Understanding your personal risk tolerance is essential. Investors often utilize a <a href="#" class="teal-link">prospectus</a> to evaluate the inherent risks of a specific mutual fund or ETF before committing capital.
    </div>

    <div class="section-title">Asset Allocation and Diversification</div>
    <div class="article-text">
        Asset allocation involves dividing an investment portfolio among different asset categories, such as equities, fixed income, and cash equivalents. The strategic goal of diversification is to mitigate systematic risk. By spreading your investments across various sectors—such as technology, healthcare, and energy—you reduce the impact of a single market downturn on your overall portfolio. This strategy is frequently managed through <a href="#" class="teal-link">index funds</a> or <a href="#" class="teal-link">mutual funds</a>.
    </div>
</div>
""", unsafe_allow_html=True)
