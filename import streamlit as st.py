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
    
    /* Expander/Accordion Styling */
    .streamlit-expanderHeader { background-color: #f8fafc; border-radius: 8px; font-weight: 600; color: #0f172a; border: 1px solid #e2e8f0; }
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
# PAGE ROUTING: LEARN (MASSIVE EDUCATIONAL HUB)
# ==========================================
elif current_page == "learn":
    st.markdown('<div class="hero-subtitle">INSTITUTIONAL KNOWLEDGE BASE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">The Master Glossary of<br><span class="hero-italic">Corporate Finance.</span></div>', unsafe_allow_html=True)
    st.write("Welcome to the institutional learning center. This repository contains advanced definitions, methodologies, and frameworks utilized by tier-one investment banks (Goldman Sachs, Morgan Stanley) during the IPO underwriting process.")
    st.divider()

    with st.expander("📌 Section 1: The IPO Lifecycle & Mechanics", expanded=True):
        st.write("""
        * **S-1 Registration Statement:** The initial, incredibly detailed document filed with the SEC by a private company planning to go public. It contains historical financials, business models, risk factors, and the proposed use of capital.
        * **The Bake-Off:** The highly competitive process where investment banks pitch the private company's management team to win the mandate of serving as the "Lead Underwriter" for the IPO.
        * **Red Herring (Preliminary Prospectus):** A draft version of the prospectus circulated to institutional investors. It contains all financial data but excludes the final IPO price and exact number of shares. The name comes from a red disclaimer printed on the cover stating the information is not yet complete.
        * **The Roadshow:** A grueling multi-city (or virtual) tour where the company’s executives and lead underwriters pitch the investment thesis to institutional investors, hedge funds, and mutual funds to generate demand.
        * **Bookbuilding:** The process during the roadshow where underwriters collect "indications of interest" from investors. If the demand exceeds the supply of shares, the "book" is considered *oversubscribed*.
        * **Greenshoe Option (Over-Allotment):** A provision in an underwriting agreement that allows the underwriters to sell up to 15% more shares than originally planned. It acts as a stabilization mechanism if the stock price skyrockets or plummets on opening day.
        * **Lock-Up Period:** A contractual caveat preventing insiders (founders, employees, early venture capitalists) from selling their shares for a specified timeframe (usually 90 to 180 days) post-IPO to prevent market flooding.
        * **Price Discovery:** The intricate mathematical and psychological process of determining the final IPO share price based on institutional demand, macroeconomic factors, and intrinsic valuation modeling.
        * **Free Float:** The actual number of shares that are freely tradable in the public market, excluding restricted shares held by insiders.
        """)

    with st.expander("📌 Section 2: Core Valuation Methodologies"):
        st.write("""
        * **Discounted Cash Flow (DCF):** The gold standard of intrinsic valuation. It involves projecting a company’s unlevered free cash flows (UFCF) 5 to 10 years into the future, and discounting them back to today's present value using the WACC.
        * **WACC (Weighted Average Cost of Capital):** The average rate of return a company is expected to pay to all its security holders to finance its assets. It serves as the discount rate in a DCF model.
        * **Terminal Value (TV):** Used in a DCF, it represents the present value of all future cash flows beyond the initial projection period, assuming the company grows at a stable rate in perpetuity.
        * **Comparable Company Analysis (Comps):** A relative valuation method that evaluates a company's metrics against publicly traded peers. If identical companies trade at 10x Revenue, the target company will likely be modeled at 10x Revenue.
        * **Precedent Transactions:** Analyzing the multiples paid in historical M&A (Mergers and Acquisitions) deals for similar companies to establish a pricing baseline.
        * **Enterprise Value (EV):** The true total value of a company. Formula: Market Capitalization + Total Debt - Cash & Cash Equivalents.
        * **Market Capitalization (Market Cap):** The total dollar market value of a company's outstanding shares of stock. Formula: Share Price × Total Number of Outstanding Shares.
        """)

    with st.expander("📌 Section 3: Advanced SaaS & Tech Fundamentals"):
        st.write("""
        * **EBITDA:** Earnings Before Interest, Taxes, Depreciation, and Amortization. A vital proxy for operational cash flow that strips out non-operating expenses.
        * **Rule of 40:** A primary benchmark for evaluating SaaS companies. It states that a software company's combined growth rate and profit margin should exceed 40%.
        * **CAC (Customer Acquisition Cost):** The total sales and marketing cost required to acquire a single new customer.
        * **LTV (Lifetime Value):** The total gross margin a company expects to earn from a customer over the duration of their relationship. An optimal LTV:CAC ratio is generally considered 3:1 or higher.
        * **ARR / MRR:** Annual/Monthly Recurring Revenue. The lifeblood of subscription businesses, representing normalized, predictable income.
        * **Net Retention Rate (NRR):** Measures the percentage of recurring revenue retained from existing customers over a given period, inclusive of upgrades, downgrades, and churn. An NRR over 100% indicates negative churn (the company grows without adding new customers).
        * **Cash Runway:** The amount of time (usually in months) a startup has before it burns through its cash reserves, assuming current burn rates remain constant.
        """)
        
    with st.expander("📌 Section 4: Macro Market Dynamics"):
        st.write("""
        * **Alpha:** The excess return of an investment relative to the return of a benchmark index. It measures portfolio manager performance.
        * **Beta:** A measure of the volatility, or systematic risk, of a security or portfolio in comparison to the market as a whole. A Beta > 1 means the stock is more volatile than the market.
        * **Systematic Risk:** Inherent risk affecting the entire market (e.g., inflation, interest rate hikes, war) that cannot be mitigated through diversification.
        * **Unsystematic Risk:** Company-specific risk (e.g., a CEO scandal, supply chain failure) that can be mitigated by holding a diversified portfolio.
        * **Liquidity Premium:** The additional return an investor demands for holding an illiquid asset (an asset that cannot be quickly converted into cash without a loss of value).
        * **VIX (Volatility Index):** Often called the "Fear Gauge," it measures the stock market's expectation of volatility based on S&P 500 index options. High VIX signals a terrible time for an IPO.
        """)
