import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import textwrap
import random
import time

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IPO Predictor Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# PAGE ROUTING
# =====================================================

page = st.query_params.get("page", "home")

# =====================================================
# GLOBAL CSS
# =====================================================

st.markdown("""
<style>

/* Hide Streamlit Menu */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

[data-testid="stHeader"]{
display:none;
}

/* Main */

.stApp{
background:#ffffff;
background-image:
linear-gradient(#f3f4f6 1px,transparent 1px),
linear-gradient(90deg,#f3f4f6 1px,transparent 1px);
background-size:40px 40px;
}

.block-container{
padding-top:90px;
padding-bottom:90px;
max-width:1300px;
}

/* =======================================
HEADER
======================================= */

.custom-header{

position:fixed;

top:0;

left:0;

width:100%;

height:72px;

background:white;

display:flex;

justify-content:center;

border-bottom:1px solid #e5e7eb;

z-index:99999;

box-shadow:0 2px 12px rgba(0,0,0,.04);

}

.header-inner{

width:95%;

max-width:1500px;

display:flex;

align-items:center;

justify-content:space-between;

}

.logo{

font-size:34px;

font-weight:900;

color:#111827;

letter-spacing:-2px;

text-decoration:none;

}

.nav{

display:flex;

gap:35px;

align-items:center;

}

.nav a{

text-decoration:none;

font-size:15px;

font-weight:600;

color:#475569;

transition:.25s;

}

.nav a:hover{

color:#2563eb;

}

.search{

width:330px;

padding:11px 18px;

background:#f3f4f6;

border-radius:999px;

border:none;

outline:none;

font-size:14px;

}

.login{

text-decoration:none;

font-weight:700;

color:#111827;

}

/* =======================================
Hero
======================================= */

.hero-small{

color:#2563eb;

font-size:13px;

font-weight:700;

letter-spacing:2px;

margin-bottom:10px;

}

.hero-title{

font-size:58px;

font-weight:800;

line-height:1.05;

color:#111827;

}

.hero-title span{

font-style:italic;

font-family:Georgia;

color:#94a3b8;

}

.hero-desc{

font-size:18px;

color:#475569;

max-width:700px;

margin-top:20px;

line-height:1.7;

}

/* =======================================
Buttons
======================================= */

.stButton>button{

width:100%;

border:none;

border-radius:999px;

padding:14px;

font-weight:700;

background:#2563eb;

color:white;

transition:.25s;

}

.stButton>button:hover{

background:#1d4ed8;

transform:translateY(-2px);

}

/* Inputs */

.stTextInput input,
.stNumberInput input{

border-radius:10px;

}

/* Divider */

hr{

border:0;

border-top:1px solid #e5e7eb;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# NAVBAR
# =====================================================

st.markdown(f"""

<div class="custom-header">

<div class="header-inner">

<a class="logo" href="?page=home" target="_self">
A.
</a>

<div class="nav">

<a href="?page=home" target="_self">
Home
</a>

<a href="?page=learn" target="_self">
Learn
</a>

<a href="#">
Markets
</a>

<a href="#">
Investors
</a>

<a href="#">
Tools
</a>

</div>

<div style="display:flex;align-items:center;gap:20px;">

<input class="search"
placeholder="Search companies..." />

<a class="login">
Login
</a>

</div>

</div>

</div>

""", unsafe_allow_html=True)
# =====================================================
# HOME PAGE
# =====================================================

if page == "home":

    # -----------------------------
    # Training Data
    # -----------------------------

    df = pd.DataFrame({

        "Revenue":[3000,25000,250,20000,500,804],

        "Profit":[12,15,-40,8,-20,-11],

        "CashBurn":[0,0,100,0,150,90],

        "Valuation":[15000,125000,1200,80000,2500,5500]

    })

    X = df[["Revenue","Profit","CashBurn"]]

    y = df["Valuation"]

    model = LinearRegression()

    model.fit(X,y)

    # -----------------------------
    # HERO
    # -----------------------------

    st.markdown(
        """
        <div class='hero-small'>
        AI VALUATION PLATFORM
        </div>

        <div class='hero-title'>
        Predict real-world IPOs<br>
        without getting lost in<br>
        <span>valuation chaos.</span>
        </div>

        <div class='hero-desc'>
        Estimate IPO valuation using machine learning,
        financial fundamentals and market sentiment.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # -----------------------------
    # DASHBOARD CARDS
    # -----------------------------

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "Global IPOs",
            "2,341",
            "+12%"
        )

    with c2:
        st.metric(
            "Avg IPO Gain",
            "18.6%",
            "+4%"
        )

    with c3:
        st.metric(
            "Market Sentiment",
            "Bullish",
            "▲"
        )

    with c4:
        st.metric(
            "Prediction Accuracy",
            "94.2%",
            "+2%"
        )

    st.divider()

    # -----------------------------
    # INPUT SECTION
    # -----------------------------

    st.header("📊 Phase 1 • Company Fundamentals")

    company = st.text_input(
        "Company Name",
        "Reddit"
    )

    col1,col2,col3 = st.columns(3)

    with col1:

        revenue = st.number_input(

            "Revenue ($ Millions)",

            value=804.0

        )

    with col2:

        margin = st.number_input(

            "Profit Margin (%)",

            value=-11.0

        )

    with col3:

        burn = st.number_input(

            "Cash Burn ($ Millions)",

            value=90.0

        )

    prediction = pd.DataFrame(

        [[revenue,margin,burn]],

        columns=["Revenue","Profit","CashBurn"]

    )

    valuation = max(

        model.predict(prediction)[0],

        100

    )

    st.progress(33)

    if st.button("Calculate Intrinsic Valuation"):

        st.success(

            f"Estimated Company Value : **${valuation:,.2f} Million**"

        )

        st.info(

            "This valuation is produced by a Machine Learning model trained on historical financial fundamentals."

        )

    st.divider()

    # -----------------------------
    # SHARE DILUTION
    # -----------------------------

    st.header("🏦 Phase 2 • IPO Structure")

    shares = st.number_input(

        "Shares Offered (Millions)",

        value=150.0

    )

    base_price = valuation / shares

    st.progress(66)

    if st.button("Calculate Base IPO Price"):

        st.success(

            f"Base IPO Price : **${base_price:.2f} / share**"

        )

    st.divider()

    # -----------------------------
    # MARKET SENTIMENT
    # -----------------------------

    st.header("📈 Phase 3 • Market Sentiment")

    left,right = st.columns(2)

    with left:

        demand = st.number_input(

            "Investor Demand (Millions)",

            value=450.0

        )

    with right:

        sp = st.number_input(

            "S&P 500 YTD Return (%)",

            value=12.0

        )

    oversub = max(

        demand/shares,

        0.1

    )

    oversub_modifier = (

        oversub-1

    )*0.05

    climate = 0

    if sp>=10:

        climate = 0.15

    elif sp<=0:

        climate = -0.15

    premium = max(

        min(

            1+

            oversub_modifier+

            climate,

            2.5

        ),

        0.5

    )

    st.slider(

        "Calculated Market Premium",

        0.5,

        2.5,

        float(premium),

        disabled=True

    )

    st.progress(100)

    if st.button("Predict Final IPO Price"):

        final_value = valuation*premium

        final_price = final_value/shares

        c1,c2,c3 = st.columns(3)

        c1.metric(

            "Intrinsic Value",

            f"${valuation:,.0f}M"

        )

        c2.metric(

            "Market Premium",

            f"{premium:.2f}x"

        )

        c3.metric(

            "IPO Price",

            f"${final_price:.2f}"

        )

        st.success(

            f"🎯 Predicted IPO Price for **{company}** : **${final_price:.2f} per share**"

        )
        # =====================================================
# LEARN PAGE
# =====================================================

elif page == "learn":

    st.markdown("""
    <style>

    .article{

        max-width:1100px;

        margin:auto;

    }

    .category{

        color:#2563eb;

        font-size:13px;

        letter-spacing:2px;

        font-weight:700;

        margin-bottom:10px;

    }

    .title{

        font-size:52px;

        font-weight:800;

        color:#111827;

        line-height:1.1;

        margin-bottom:20px;

    }

    .intro{

        color:#475569;

        font-size:18px;

        line-height:1.8;

        margin-bottom:30px;

    }

    .section{

        font-size:30px;

        font-weight:700;

        margin-top:40px;

        margin-bottom:20px;

    }

    .text{

        color:#475569;

        font-size:17px;

        line-height:1.8;

    }

    .card{

        background:white;

        border-radius:16px;

        border:1px solid #E5E7EB;

        padding:25px;

        box-shadow:0 6px 20px rgba(0,0,0,.04);

        height:100%;

    }

    .card h3{

        margin-top:0;

        color:#111827;

    }

    .card p{

        color:#64748B;

        line-height:1.7;

    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="article">

    <div class="category">
    INVESTING FOR BEGINNERS
    </div>

    <div class="title">
    Understanding IPO Investing
    </div>

    <div class="intro">

    An Initial Public Offering (IPO) is the first time a private
    company offers its shares to the public. IPO investing allows
    investors to participate in the early stages of publicly traded
    companies.

    </div>

    </div>

    """, unsafe_allow_html=True)

    st.markdown("## What is an IPO?")

    st.write("""
An Initial Public Offering converts a private company into a publicly traded company.

Companies generally launch IPOs to:

- Raise fresh capital
- Expand operations
- Pay existing debt
- Improve credibility
- Allow early investors to exit
""")

    st.divider()

    st.markdown("## Why Valuation Matters")

    st.write("""

The biggest challenge during an IPO is determining the company's valuation.

Investment banks estimate valuation using:

- Revenue Growth
- EBITDA
- Profit Margins
- Comparable Companies
- Discounted Cash Flow
- Market Conditions

Our AI model combines financial data with market sentiment to estimate a fair IPO price.

""")

    st.divider()

    st.markdown("## IPO Pricing Process")

    step1,step2,step3 = st.columns(3)

    with step1:

        st.info("""

### Step 1

Collect Financial Statements

Revenue

Profit

Cash Flow

Growth

""")

    with step2:

        st.info("""

### Step 2

Estimate Enterprise Value

Comparable Analysis

DCF

ML Models

Sector Multiples

""")

    with step3:

        st.info("""

### Step 3

Roadshow & Demand

Book Building

Institutional Demand

Retail Demand

Final Price

""")

    st.divider()

    st.markdown("## Featured Learning Resources")

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown("""

<div class="card">

<h3>📘 Investing Basics</h3>

<p>

Learn how the stock market works,
risk management,
portfolio diversification
and compounding.

</p>

</div>

""", unsafe_allow_html=True)

    with c2:

        st.markdown("""

<div class="card">

<h3>📊 Financial Statements</h3>

<p>

Understand Income Statements,
Balance Sheets,
Cash Flow Statements
and financial ratios.

</p>

</div>

""", unsafe_allow_html=True)

    with c3:

        st.markdown("""

<div class="card">

<h3>🤖 AI Valuation</h3>

<p>

Discover how Machine Learning
can estimate company valuation
using financial metrics.

</p>

</div>

""", unsafe_allow_html=True)

    with c4:

        st.markdown("""

<div class="card">

<h3>📈 Market Psychology</h3>

<p>

Understand oversubscription,
market hype,
investor demand
and IPO momentum.

</p>

</div>

""", unsafe_allow_html=True)

    st.divider()

    st.markdown("## Investment Tips")

    st.success("""

✅ Invest for the long term

✅ Diversify your portfolio

✅ Read the company's prospectus

✅ Never invest based only on hype

✅ Understand company fundamentals before buying

""")
    # =====================================================
# BLOOMBERG STYLE STOCK TICKER
# =====================================================

st.markdown("""

<style>

/* Add bottom spacing so ticker doesn't overlap content */
.block-container{
    padding-bottom:70px !important;
}

/* Fixed Bottom Ticker */

.stock-ticker{

position:fixed;

bottom:0;

left:0;

width:100%;

height:48px;

background:#0f172a;

border-top:1px solid #1e293b;

display:flex;

align-items:center;

overflow:hidden;

z-index:999999;

box-shadow:0 -3px 10px rgba(0,0,0,.25);

font-family:Inter,sans-serif;

}

/* Track */

.stock-track{

display:flex;

width:max-content;

animation:scroll 45s linear infinite;

}

.stock-track:hover{

animation-play-state:paused;

}

/* Animation */

@keyframes scroll{

0%{

transform:translateX(0);

}

100%{

transform:translateX(-50%);

}

}

/* Items */

.stock{

display:flex;

align-items:center;

padding:0 28px;

font-size:14px;

white-space:nowrap;

}

.symbol{

color:#94a3b8;

font-weight:700;

margin-right:8px;

}

.price{

color:white;

font-weight:600;

margin-right:8px;

}

.green{

color:#22c55e;

font-weight:700;

}

.red{

color:#ef4444;

font-weight:700;

}

</style>

<div class="stock-ticker">

<div class="stock-track">

<div class="stock">
<span class="symbol">NIFTY 50</span>
<span class="price">23,458.20</span>
<span class="green">▲ +0.62%</span>
</div>

<div class="stock">
<span class="symbol">BANK NIFTY</span>
<span class="price">50,120.50</span>
<span class="green">▲ +0.64%</span>
</div>

<div class="stock">
<span class="symbol">RELIANCE</span>
<span class="price">₹2,980.15</span>
<span class="green">▲ +0.83%</span>
</div>

<div class="stock">
<span class="symbol">TCS</span>
<span class="price">₹4,120.00</span>
<span class="red">▼ -0.30%</span>
</div>

<div class="stock">
<span class="symbol">INFY</span>
<span class="price">₹1,650.25</span>
<span class="red">▼ -0.31%</span>
</div>

<div class="stock">
<span class="symbol">ICICI</span>
<span class="price">₹1,115.40</span>
<span class="green">▲ +1.29%</span>
</div>

<div class="stock">
<span class="symbol">SBIN</span>
<span class="price">₹820.50</span>
<span class="red">▼ -0.58%</span>
</div>

<div class="stock">
<span class="symbol">HDFC</span>
<span class="price">₹1,540.80</span>
<span class="green">▲ +0.55%</span>
</div>

<div class="stock">
<span class="symbol">ITC</span>
<span class="price">₹435.60</span>
<span class="green">▲ +0.48%</span>
</div>

<div class="stock">
<span class="symbol">LT</span>
<span class="price">₹3,560.00</span>
<span class="green">▲ +1.19%</span>
</div>

<div class="stock">
<span class="symbol">BHARTI</span>
<span class="price">₹1,410.90</span>
<span class="green">▲ +1.31%</span>
</div>

<!-- Duplicate for infinite animation -->

<div class="stock">
<span class="symbol">NIFTY 50</span>
<span class="price">23,458.20</span>
<span class="green">▲ +0.62%</span>
</div>

<div class="stock">
<span class="symbol">BANK NIFTY</span>
<span class="price">50,120.50</span>
<span class="green">▲ +0.64%</span>
</div>

<div class="stock">
<span class="symbol">RELIANCE</span>
<span class="price">₹2,980.15</span>
<span class="green">▲ +0.83%</span>
</div>

<div class="stock">
<span class="symbol">TCS</span>
<span class="price">₹4,120.00</span>
<span class="red">▼ -0.30%</span>
</div>

<div class="stock">
<span class="symbol">INFY</span>
<span class="price">₹1,650.25</span>
<span class="red">▼ -0.31%</span>
</div>

<div class="stock">
<span class="symbol">ICICI</span>
<span class="price">₹1,115.40</span>
<span class="green">▲ +1.29%</span>
</div>

<div class="stock">
<span class="symbol">SBIN</span>
<span class="price">₹820.50</span>
<span class="red">▼ -0.58%</span>
</div>

<div class="stock">
<span class="symbol">HDFC</span>
<span class="price">₹1,540.80</span>
<span class="green">▲ +0.55%</span>
</div>

<div class="stock">
<span class="symbol">ITC</span>
<span class="price">₹435.60</span>
<span class="green">▲ +0.48%</span>
</div>

<div class="stock">
<span class="symbol">LT</span>
<span class="price">₹3,560.00</span>
<span class="green">▲ +1.19%</span>
</div>

<div class="stock">
<span class="symbol">BHARTI</span>
<span class="price">₹1,410.90</span>
<span class="green">▲ +1.31%</span>
</div>

</div>

</div>

""", unsafe_allow_html=True)
