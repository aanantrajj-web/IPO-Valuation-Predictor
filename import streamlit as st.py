import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
import random
import time

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="X-Invo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# PAGE ROUTING
# ==========================================================

page = st.query_params.get("page", "home")

# ==========================================================
# GLOBAL CSS
# ==========================================================

st.markdown("""
<style>

/* Hide Streamlit */

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

/* Font */

html,
body,
[class*="css"]{
font-family:Inter,sans-serif;
}

/* Background */

.stApp{

background:#fafafa;

background-image:

linear-gradient(#eeeeee 1px,transparent 1px),

linear-gradient(90deg,#eeeeee 1px,transparent 1px);

background-size:40px 40px;

}

/* Main Container */

.block-container{

padding-top:130px;

padding-bottom:90px;

max-width:1400px;

}

/* ==========================================================
TOP STRIP
========================================================== */

.top-strip{

position:fixed;

top:0;

left:0;

width:100%;

height:30px;

background:#000;

display:flex;

justify-content:center;

align-items:center;

z-index:99999;

border-bottom:1px solid #202020;

}

.top-inner{

width:96%;

max-width:1700px;

display:flex;

gap:28px;

}

.top-inner a{

color:#b8b8b8;

font-size:13px;

text-decoration:none;

transition:.2s;

}

.top-inner a:hover{

color:white;

}

/* ==========================================================
HEADER
========================================================== */

.main-header{

position:fixed;

top:30px;

left:0;

width:100%;

height:72px;

background:#000;

display:flex;

justify-content:center;

align-items:center;

z-index:99998;

border-bottom:1px solid #202020;

}

.main-inner{

width:96%;

max-width:1700px;

display:flex;

justify-content:space-between;

align-items:center;

}

/* Logo */

.logo{

font-size:52px;

font-weight:900;

color:white;

letter-spacing:-2px;

user-select:none;

}

.logo span{

color:#ff9d00;

}

/* Navigation */

.nav{

display:flex;

gap:32px;

align-items:center;

}

.nav a{

color:white;

text-decoration:none;

font-size:17px;

font-weight:500;

transition:.25s;

}

.nav a:hover{

color:#ff9d00;

}

/* Right */

.right{

display:flex;

align-items:center;

gap:18px;

}

.login{

color:white;

font-weight:700;

cursor:pointer;

}

.subscribe{

background:white;

color:black;

padding:9px 18px;

border-radius:4px;

font-weight:700;

cursor:pointer;

transition:.2s;

}

.subscribe:hover{

background:#ff9d00;

}

.search{

font-size:24px;

color:white;

cursor:pointer;

}

/* ==========================================================
HEADINGS
========================================================== */

.hero-small{

color:#2563eb;

font-size:14px;

font-weight:700;

letter-spacing:2px;

margin-bottom:8px;

}

.hero-title{

font-size:62px;

font-weight:900;

line-height:1.05;

color:#111827;

margin-bottom:18px;

}

.hero-title span{

font-family:Georgia;

font-style:italic;

color:#94a3b8;

}

.hero-text{

font-size:18px;

line-height:1.8;

color:#475569;

max-width:700px;

}

/* Buttons */

.stButton>button{

background:#2563eb;

color:white;

border:none;

border-radius:999px;

padding:14px;

font-weight:700;

width:100%;

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

/* Cards */

.metric-card{

background:white;

padding:22px;

border-radius:16px;

border:1px solid #E5E7EB;

box-shadow:0 5px 16px rgba(0,0,0,.05);

}

/* Divider */

hr{

border:none;

border-top:1px solid #E5E7EB;

margin:30px 0;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
HEADER
# ==========================================================

st.markdown("""

<div class="top-strip">

<div class="top-inner">

<a href="#">Documentation</a>

<a href="#">API</a>

<a href="#">Pricing</a>

<a href="#">Enterprise</a>

<a href="#">Support</a>

</div>

</div>

<div class="main-header">

<div class="main-inner">

<div class="logo">

X<span>-</span>Invo

</div>

<div class="nav">

<a href="?page=home" target="_self">Home</a>

<a href="?page=predictor" target="_self">IPO Predictor</a>

<a href="?page=markets" target="_self">Markets</a>

<a href="?page=news" target="_self">News</a>

<a href="?page=learn" target="_self">Learn</a>

<a href="?page=tools" target="_self">Tools</a>

</div>

<div class="right">

<div class="login">

Sign In

</div>

<div class="subscribe">

Subscribe

</div>

<div class="search">

🔍

</div>

</div>

</div>

</div>

""", unsafe_allow_html=True)
# ==========================================================
# HOME PAGE
# ==========================================================

if page == "home":

    st.markdown("""
    <style>

    .hero-wrapper{

        display:flex;

        align-items:center;

        justify-content:space-between;

        gap:60px;

        margin-top:30px;

        margin-bottom:70px;

    }

    .hero-left{

        flex:1;

    }

    .hero-right{

        flex:1;

    }

    .hero-badge{

        display:inline-block;

        background:#E0F2FE;

        color:#2563EB;

        padding:8px 16px;

        border-radius:999px;

        font-weight:700;

        font-size:13px;

        margin-bottom:20px;

    }

    .dashboard-card{

        background:white;

        border-radius:18px;

        padding:25px;

        border:1px solid #E5E7EB;

        box-shadow:0 10px 25px rgba(0,0,0,.05);

    }

    .big-number{

        font-size:34px;

        font-weight:800;

        color:#111827;

    }

    .green{

        color:#16A34A;

        font-weight:700;

    }

    .red{

        color:#DC2626;

        font-weight:700;

    }

    </style>

    """, unsafe_allow_html=True)

    # ---------------- HERO ----------------

    left,right = st.columns([1.2,1])

    with left:

        st.markdown("""
        <div class="hero-badge">
        AI Powered IPO Intelligence
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-title">

        Predict IPO Prices<br>

        Before The Market<br>

        <span>Prices Them.</span>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-text">

        X-Invo combines Machine Learning,
        financial fundamentals,
        institutional demand,
        and market sentiment
        to estimate a company's fair IPO valuation.

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        colA,colB = st.columns(2)

        with colA:

            st.button("🚀 Start Prediction")

        with colB:

            st.button("📘 Learn IPOs")

    with right:

        st.markdown("""
        <div class="dashboard-card">

        <h3>Market Snapshot</h3>

        """, unsafe_allow_html=True)

        m1,m2 = st.columns(2)

        with m1:

            st.metric(
                "NIFTY 50",
                "23,458",
                "+0.62%"
            )

            st.metric(
                "NASDAQ",
                "18,972",
                "+1.13%"
            )

        with m2:

            st.metric(
                "SENSEX",
                "77,824",
                "+0.59%"
            )

            st.metric(
                "Dow Jones",
                "42,180",
                "-0.24%"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # =====================================================
    # QUICK STATS
    # =====================================================

    a,b,c,d = st.columns(4)

    with a:

        st.metric(
            "Companies Analysed",
            "5,284",
            "+182"
        )

    with b:

        st.metric(
            "Prediction Accuracy",
            "94.8%",
            "+2.1%"
        )

    with c:

        st.metric(
            "Average IPO Gain",
            "18.6%",
            "+4.8%"
        )

    with d:

        st.metric(
            "Market Mood",
            "Bullish",
            "▲"
        )

    st.divider()

    # =====================================================
    # FEATURED IPOs
    # =====================================================

    st.subheader("🔥 Trending IPOs")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="dashboard-card">

        <h3>Stripe</h3>

        <p>Expected Valuation</p>

        <div class="big-number">

        $92B

        </div>

        <br>

        <span class="green">

        Strong Demand ▲

        </span>

        </div>

        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="dashboard-card">

        <h3>Databricks</h3>

        <p>Expected Valuation</p>

        <div class="big-number">

        $62B

        </div>

        <br>

        <span class="green">

        High Institutional Interest

        </span>

        </div>

        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="dashboard-card">

        <h3>SpaceX</h3>

        <p>Expected Valuation</p>

        <div class="big-number">

        $210B

        </div>

        <br>

        <span class="green">

        Exceptional Growth

        </span>

        </div>

        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Why X-Invo?")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.info("""

### 🤖 AI Valuation

Uses Machine Learning to estimate intrinsic company valuation from financial metrics.

""")

    with c2:

        st.info("""

### 📈 Market Sentiment

Adjusts IPO pricing using investor demand and market conditions.

""")

    with c3:

        st.info("""

### ⚡ Real-Time Dashboard

Track valuations, IPOs and market activity in one place.

""")

    st.divider()
    # ==========================================================
# IPO PREDICTOR PAGE
# ==========================================================

elif page == "predictor":

    st.title("📈 IPO Predictor")

    st.caption(
        "Estimate an IPO price using financial fundamentals and market sentiment."
    )

    st.divider()

    # -------------------------------------------------------
    # TRAINING DATA
    # -------------------------------------------------------

    training = pd.DataFrame({

        "Revenue":[
            3000,
            25000,
            250,
            20000,
            500,
            804,
            1200,
            5000
        ],

        "ProfitMargin":[
            12,
            15,
            -40,
            8,
            -20,
            -11,
            6,
            14
        ],

        "CashBurn":[
            0,
            0,
            100,
            0,
            150,
            90,
            40,
            0
        ],

        "Valuation":[
            15000,
            125000,
            1200,
            80000,
            2500,
            5500,
            8500,
            31000
        ]

    })

    X = training[
        ["Revenue","ProfitMargin","CashBurn"]
    ]

    y = training["Valuation"]

    model = LinearRegression()

    model.fit(X,y)

    # -------------------------------------------------------
    # INPUTS
    # -------------------------------------------------------

    st.subheader("Phase 1 • Financial Fundamentals")

    company = st.text_input(
        "Company Name",
        "Reddit"
    )

    c1,c2,c3 = st.columns(3)

    with c1:

        revenue = st.number_input(
            "Revenue ($ Millions)",
            min_value=0.0,
            value=804.0
        )

    with c2:

        margin = st.number_input(
            "Profit Margin (%)",
            value=-11.0
        )

    with c3:

        burn = st.number_input(
            "Cash Burn ($ Millions)",
            min_value=0.0,
            value=90.0
        )

    input_df = pd.DataFrame(

        [[
            revenue,
            margin,
            burn
        ]],

        columns=[
            "Revenue",
            "ProfitMargin",
            "CashBurn"
        ]

    )

    intrinsic = max(
        model.predict(input_df)[0],
        100
    )

    if st.button("Calculate Intrinsic Valuation"):

        st.success(
            f"Intrinsic Valuation: ${intrinsic:,.2f} Million"
        )

    st.divider()

    # -------------------------------------------------------
    # SHARE OFFER
    # -------------------------------------------------------

    st.subheader("Phase 2 • IPO Structure")

    shares = st.number_input(

        "Shares Offered (Millions)",

        min_value=1.0,

        value=150.0

    )

    base_price = intrinsic / shares

    if st.button("Calculate Base IPO Price"):

        st.success(

            f"Base IPO Price : ${base_price:.2f}"

        )

    st.divider()

    # -------------------------------------------------------
    # MARKET SENTIMENT
    # -------------------------------------------------------

    st.subheader("Phase 3 • Supply & Demand")

    left,right = st.columns(2)

    with left:

        demand = st.number_input(

            "Investor Demand (Millions)",

            value=450.0

        )

    with right:

        market = st.slider(

            "Overall Market Mood",

            -20,

            20,

            12

        )

    oversub = max(

        demand/shares,

        0.1

    )

    oversub_modifier = (

        oversub-1

    )*0.05

    climate = 0

    if market >= 10:

        climate = 0.15

    elif market <= 0:

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

        "Market Premium",

        0.5,

        2.5,

        float(premium),

        disabled=True

    )

    final_value = intrinsic*premium

    final_price = final_value/shares

    if st.button("Predict IPO Price"):

        a,b,c = st.columns(3)

        with a:

            st.metric(

                "Intrinsic Value",

                f"${intrinsic:,.0f} M"

            )

        with b:

            st.metric(

                "Market Premium",

                f"{premium:.2f}x"

            )

        with c:

            st.metric(

                "Predicted IPO",

                f"${final_price:.2f}"

            )

        st.success(

            f"Predicted IPO Price for {company}: ${final_price:.2f}"

        )

    st.divider()

    # -------------------------------------------------------
    # CHART
    # -------------------------------------------------------

    chart = pd.DataFrame({

        "Stage":[

            "Intrinsic",

            "Adjusted"

        ],

        "Valuation":[

            intrinsic,

            final_value

        ]

    })

    fig = px.bar(

        chart,

        x="Stage",

        y="Valuation",

        text="Valuation",

        color="Stage"

    )

    fig.update_layout(

        height=420,

        template="plotly_white",

        showlegend=False

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )
    # ==========================================================
# MARKETS PAGE
# ==========================================================

elif page == "markets":

    st.title("🌍 Global Markets Dashboard")

    st.caption("Track major indices, sectors and market activity.")

    st.divider()

    # ======================================================
    # TOP MARKET METRICS
    # ======================================================

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "NIFTY 50",
            "23,458.20",
            "+145.30"
        )

    with c2:
        st.metric(
            "SENSEX",
            "77,824.12",
            "+410.55"
        )

    with c3:
        st.metric(
            "NASDAQ",
            "18,975.10",
            "+185.40"
        )

    with c4:
        st.metric(
            "Dow Jones",
            "42,180.40",
            "-82.10"
        )

    st.divider()

    # ======================================================
    # MARKET PERFORMANCE CHART
    # ======================================================

    st.subheader("Market Performance")

    dates = pd.date_range("2026-01-01", periods=30)

    values = np.cumsum(np.random.normal(0.8, 8, 30)) + 23000

    market_df = pd.DataFrame({
        "Date": dates,
        "Index": values
    })

    fig = px.line(
        market_df,
        x="Date",
        y="Index",
        template="plotly_white"
    )

    fig.update_traces(line_width=3)

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # SECTOR PERFORMANCE
    # ======================================================

    st.subheader("Sector Performance")

    sector_df = pd.DataFrame({

        "Sector":[
            "Technology",
            "Finance",
            "Healthcare",
            "Energy",
            "FMCG",
            "Automobile"
        ],

        "Return":[
            18,
            12,
            9,
            6,
            4,
            11
        ]

    })

    fig = px.bar(

        sector_df,

        x="Sector",

        y="Return",

        color="Return",

        template="plotly_white"

    )

    fig.update_layout(
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # PORTFOLIO DISTRIBUTION
    # ======================================================

    left,right = st.columns(2)

    with left:

        st.subheader("Market Capitalization")

        pie = px.pie(

            names=[
                "Large Cap",
                "Mid Cap",
                "Small Cap"
            ],

            values=[
                62,
                23,
                15
            ],

            hole=.45

        )

        pie.update_layout(
            height=400
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with right:

        st.subheader("Top Gainers")

        gainers = pd.DataFrame({

            "Company":[
                "Reliance",
                "Infosys",
                "ICICI Bank",
                "L&T",
                "Tata Motors"
            ],

            "Gain (%)":[
                4.2,
                3.7,
                3.1,
                2.9,
                2.8
            ]

        })

        st.dataframe(
            gainers,
            use_container_width=True
        )

    st.divider()

    # ======================================================
    # IPO CALENDAR
    # ======================================================

    st.subheader("Upcoming IPO Calendar")

    ipo = pd.DataFrame({

        "Company":[
            "Stripe",
            "Databricks",
            "Discord",
            "Canva",
            "SpaceX"
        ],

        "Expected Month":[
            "August",
            "September",
            "October",
            "November",
            "December"
        ],

        "Expected Valuation ($B)":[
            92,
            62,
            18,
            40,
            210
        ]

    })

    st.dataframe(
        ipo,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # MARKET NEWS
    # ======================================================

    st.subheader("Today's Highlights")

    news1,news2 = st.columns(2)

    with news1:

        st.info("""

### 📈 Technology Stocks Rally

Technology companies continue leading market gains amid
strong quarterly earnings and increased AI investments.

""")

    with news2:

        st.info("""

### 💰 IPO Market Reopens

Several billion-dollar startups are expected to launch IPOs
over the coming months.

""")
        # ==========================================================
# NEWS PAGE
# ==========================================================

elif page == "news":

    st.title("📰 Financial News")

    st.caption(
        "Latest market news, IPO updates and financial insights."
    )

    st.divider()

    # ======================================================
    # SEARCH
    # ======================================================

    search = st.text_input(
        "🔍 Search News",
        placeholder="Search companies or topics..."
    )

    st.write("")

    # ======================================================
    # FEATURED STORY
    # ======================================================

    st.markdown("""
    <div style="
        background:#111827;
        color:white;
        padding:35px;
        border-radius:18px;
        margin-bottom:25px;
    ">
        <h2 style="margin-bottom:10px;">
        🚀 AI Companies Continue Leading IPO Wave
        </h2>

        <p style="font-size:17px;line-height:1.8;">
        Investor demand for artificial intelligence startups remains
        exceptionally strong. Analysts expect several billion-dollar
        IPOs during the next twelve months.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ======================================================
    # TOP STORIES
    # ======================================================

    st.subheader("Top Stories")

    c1,c2 = st.columns(2)

    with c1:

        st.container(border=True)

        st.markdown("### 📈 Markets Close Higher")

        st.write("""
Technology and banking stocks pushed
major indices higher after strong
earnings reports.
""")

        st.caption("2 hours ago")

    with c2:

        st.container(border=True)

        st.markdown("### 💰 IPO Pipeline Expands")

        st.write("""
Investment banks expect more than
30 major IPOs over the coming year.
""")

        st.caption("3 hours ago")

    st.write("")

    c3,c4 = st.columns(2)

    with c3:

        st.container(border=True)

        st.markdown("### 🤖 AI Sector Outperforms")

        st.write("""
Artificial Intelligence companies
continue outperforming traditional
technology firms.
""")

        st.caption("5 hours ago")

    with c4:

        st.container(border=True)

        st.markdown("### 🌎 Global Markets Mixed")

        st.write("""
European markets remained flat while
US technology stocks gained.
""")

        st.caption("6 hours ago")

    st.divider()

    # ======================================================
    # MARKET MOVERS
    # ======================================================

    st.subheader("Today's Market Movers")

    movers = pd.DataFrame({

        "Company":[
            "NVIDIA",
            "Apple",
            "Microsoft",
            "Reliance",
            "Infosys",
            "TCS",
            "ICICI Bank",
            "Amazon",
            "Tesla",
            "Meta"
        ],

        "Price":[
            1298,
            214,
            485,
            2980,
            1650,
            4120,
            1115,
            198,
            312,
            615
        ],

        "Change %":[
            5.8,
            2.4,
            1.9,
            0.8,
            -0.3,
            -0.4,
            1.2,
            2.1,
            3.4,
            2.7
        ]

    })

    st.dataframe(
        movers,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================================
    # TRENDING TOPICS
    # ======================================================

    st.subheader("Trending Topics")

    a,b,c,d = st.columns(4)

    with a:
        st.success("AI")

    with b:
        st.success("IPO")

    with c:
        st.success("NVIDIA")

    with d:
        st.success("Interest Rates")

    st.divider()

    # ======================================================
    # EDITOR PICKS
    # ======================================================

    st.subheader("Editor's Picks")

    articles = [

        {
            "title":"How IPO Valuation Works",
            "time":"8 min read"
        },

        {
            "title":"Understanding P/E Ratio",
            "time":"6 min read"
        },

        {
            "title":"DCF Valuation Explained",
            "time":"10 min read"
        },

        {
            "title":"Machine Learning in Finance",
            "time":"12 min read"
        }

    ]

    for item in articles:

        st.markdown(f"""
        <div style="
        background:white;
        padding:20px;
        border-radius:14px;
        border:1px solid #E5E7EB;
        margin-bottom:12px;
        ">
        <h4>{item['title']}</h4>
        <p>{item['time']}</p>
        </div>
        """, unsafe_allow_html=True)
        # ==========================================================
# LEARN PAGE
# ==========================================================

elif page == "learn":

    st.title("📚 X-Invo Academy")

    st.caption(
        "Master Investing, IPOs and Financial Analysis."
    )

    st.divider()

    # ======================================================
    # HERO
    # ======================================================

    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#0F172A,#1E293B);
    padding:45px;
    border-radius:18px;
    color:white;
    margin-bottom:30px;
    ">
    <h1 style="margin-bottom:15px;">
    Learn Investing From Scratch
    </h1>

    <p style="font-size:18px;line-height:1.8;">
    Whether you're a beginner or an experienced investor,
    X-Invo Academy teaches everything from financial
    statements to IPO valuation using interactive examples.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ======================================================
    # LEARNING PATH
    # ======================================================

    st.subheader("Learning Roadmap")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.success("""
### Level 1

Stock Market Basics

• Shares

• Exchanges

• Investors

""")

    with c2:
        st.success("""
### Level 2

Financial Statements

• Revenue

• Profit

• Cash Flow

""")

    with c3:
        st.success("""
### Level 3

Valuation

• P/E Ratio

• DCF

• Comparable Analysis

""")

    with c4:
        st.success("""
### Level 4

IPO Investing

• Book Building

• Premium

• Listing Gain

""")

    st.divider()

    # ======================================================
    # COURSES
    # ======================================================

    st.subheader("Featured Courses")

    a,b,c = st.columns(3)

    with a:

        st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:15px;
border:1px solid #E5E7EB;
">

## 📈 Stock Market

Learn how stock markets operate.

⭐ Beginner

⏱ 4 Hours

</div>
""", unsafe_allow_html=True)

    with b:

        st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:15px;
border:1px solid #E5E7EB;
">

## 💰 Company Valuation

Master valuation techniques.

⭐ Intermediate

⏱ 6 Hours

</div>
""", unsafe_allow_html=True)

    with c:

        st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:15px;
border:1px solid #E5E7EB;
">

## 🚀 IPO Analysis

Predict IPO pricing using AI.

⭐ Advanced

⏱ 5 Hours

</div>
""", unsafe_allow_html=True)

    st.divider()

    # ======================================================
    # FINANCE GLOSSARY
    # ======================================================

    st.subheader("Finance Glossary")

    glossary = pd.DataFrame({

        "Term":[

            "Revenue",

            "EBITDA",

            "P/E Ratio",

            "Cash Burn",

            "Market Cap",

            "Book Value",

            "Intrinsic Value",

            "IPO"

        ],

        "Meaning":[

            "Company Sales",

            "Operating Earnings",

            "Price to Earnings",

            "Cash Spent Per Period",

            "Company Value",

            "Net Asset Value",

            "True Estimated Worth",

            "Initial Public Offering"

        ]

    })

    st.dataframe(
        glossary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================================
    # VIDEO LESSONS
    # ======================================================

    st.subheader("Recommended Lessons")

    x,y = st.columns(2)

    with x:

        st.info("""

### 🎥 Understanding IPOs

Duration: 18 mins

Difficulty: Beginner

""")

    with y:

        st.info("""

### 🎥 Reading Balance Sheets

Duration: 24 mins

Difficulty: Intermediate

""")

    st.divider()

    # ======================================================
    # QUIZ
    # ======================================================

    st.subheader("Quick Quiz")

    q = st.radio(

        "What does IPO stand for?",

        [

            "International Purchase Order",

            "Initial Public Offering",

            "Internal Pricing Option",

            "Investment Purchase Opportunity"

        ]

    )

    if st.button("Check Answer"):

        if q == "Initial Public Offering":

            st.success("✅ Correct!")

        else:

            st.error("❌ Incorrect. The correct answer is Initial Public Offering.")

    st.divider()

    # ======================================================
    # CERTIFICATION
    # ======================================================

    st.subheader("Complete Your Learning")

    progress = st.progress(72)

    st.write("Course Progress: **72%**")

    st.button("Continue Learning →")
    # ==========================================================
# TOOLS PAGE
# ==========================================================

elif page == "tools":

    st.title("🧮 Financial Tools")

    st.caption(
        "Professional calculators for investors and analysts."
    )

    st.divider()

    tool = st.selectbox(
        "Choose a Calculator",
        [
            "DCF Calculator",
            "CAGR Calculator",
            "Compound Interest",
            "SIP Calculator",
            "Financial Ratios"
        ]
    )

    # =====================================================
    # DCF
    # =====================================================

    if tool == "DCF Calculator":

        st.subheader("Discounted Cash Flow")

        col1,col2,col3 = st.columns(3)

        with col1:
            cashflow = st.number_input(
                "Annual Free Cash Flow ($M)",
                value=500.0
            )

        with col2:
            growth = st.slider(
                "Growth Rate (%)",
                0,
                30,
                10
            )

        with col3:
            discount = st.slider(
                "Discount Rate (%)",
                1,
                20,
                10
            )

        years = 5

        total = 0

        for i in range(1, years+1):

            future = cashflow*((1+growth/100)**i)

            pv = future/((1+discount/100)**i)

            total += pv

        st.success(
            f"Estimated DCF Valuation: ${total:,.2f} Million"
        )

    # =====================================================
    # CAGR
    # =====================================================

    elif tool == "CAGR Calculator":

        st.subheader("Compound Annual Growth Rate")

        c1,c2,c3 = st.columns(3)

        with c1:
            begin = st.number_input(
                "Beginning Value",
                value=100
            )

        with c2:
            end = st.number_input(
                "Ending Value",
                value=250
            )

        with c3:
            yrs = st.number_input(
                "Years",
                value=5
            )

        cagr = ((end/begin)**(1/yrs)-1)*100

        st.metric(
            "CAGR",
            f"{cagr:.2f}%"
        )

    # =====================================================
    # COMPOUND INTEREST
    # =====================================================

    elif tool == "Compound Interest":

        st.subheader("Compound Interest Calculator")

        p = st.number_input(
            "Principal",
            value=10000
        )

        r = st.slider(
            "Interest Rate (%)",
            1,
            20,
            8
        )

        n = st.number_input(
            "Years",
            value=10
        )

        amount = p*((1+r/100)**n)

        st.metric(
            "Future Value",
            f"${amount:,.2f}"
        )

    # =====================================================
    # SIP
    # =====================================================

    elif tool == "SIP Calculator":

        st.subheader("Systematic Investment Plan")

        monthly = st.number_input(
            "Monthly Investment",
            value=500
        )

        rate = st.slider(
            "Expected Return (%)",
            1,
            20,
            12
        )

        yrs = st.number_input(
            "Years",
            value=15
        )

        months = yrs*12

        monthly_rate = rate/1200

        future = monthly*(((1+monthly_rate)**months-1)/monthly_rate)*(1+monthly_rate)

        st.metric(
            "Estimated Corpus",
            f"${future:,.2f}"
        )

    # =====================================================
    # RATIOS
    # =====================================================

    elif tool == "Financial Ratios":

        st.subheader("Financial Ratio Calculator")

        revenue = st.number_input(
            "Revenue",
            value=1000.0
        )

        profit = st.number_input(
            "Net Profit",
            value=150.0
        )

        assets = st.number_input(
            "Total Assets",
            value=3000.0
        )

        equity = st.number_input(
            "Shareholder Equity",
            value=1800.0
        )

        margin = (profit/revenue)*100

        roa = (profit/assets)*100

        roe = (profit/equity)*100

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
                "Profit Margin",
                f"{margin:.2f}%"
            )

        with c2:
            st.metric(
                "ROA",
                f"{roa:.2f}%"
            )

        with c3:
            st.metric(
                "ROE",
                f"{roe:.2f}%"
            )

    st.divider()

    st.subheader("📈 Financial Formula Reference")

    formulas = {
        "DCF":
        "PV = CF / (1+r)^n",

        "CAGR":
        "((Ending/Beginning)^(1/n))-1",

        "Compound Interest":
        "A=P(1+r)^n",

        "ROE":
        "Net Profit / Equity",

        "ROA":
        "Net Profit / Assets"
    }

    st.table(pd.DataFrame(
        formulas.items(),
        columns=["Formula","Expression"]
    ))
    # ==========================================================
# PART 8 - FINAL UI POLISH
# Bloomberg-style Ticker + Footer
# ==========================================================

import datetime

# ----------------------------------------------------------
# Additional CSS
# ----------------------------------------------------------
st.markdown("""
<style>

/* Bottom ticker */

.bottom-ticker{
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    height:42px;
    background:#000000;
    color:#F59E0B;
    overflow:hidden;
    white-space:nowrap;
    z-index:99999;
    border-top:2px solid #F59E0B;
    font-size:15px;
    font-weight:600;
    display:flex;
    align-items:center;
}

.bottom-ticker span{
    display:inline-block;
    padding-left:100%;
    animation:ticker 40s linear infinite;
}

@keyframes ticker{

0%{
transform:translateX(0);
}

100%{
transform:translateX(-100%);
}

}

/* Footer */

.footer{

margin-top:80px;
margin-bottom:55px;
padding:25px;

border-top:1px solid #D1D5DB;

text-align:center;

color:#6B7280;

font-size:14px;

}

.footer h4{

margin-bottom:8px;

color:#111827;

}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# Loading animation
# ----------------------------------------------------------

with st.spinner("Loading X-Invo Dashboard..."):
    time.sleep(0.4)

# ----------------------------------------------------------
# Live ticker
# ----------------------------------------------------------

ticker_html = """
<div class="bottom-ticker">

<span>

📈 NIFTY 50 ▲ 23,458.20 (+0.62%)
&nbsp;&nbsp;&nbsp;&nbsp;

📊 SENSEX ▲ 77,824.12 (+0.53%)
&nbsp;&nbsp;&nbsp;&nbsp;

💻 NASDAQ ▲ 18,975.10 (+1.12%)
&nbsp;&nbsp;&nbsp;&nbsp;

🏦 DOW JONES ▼ 42,180.40 (-0.19%)
&nbsp;&nbsp;&nbsp;&nbsp;

🚀 NVIDIA ▲ 4.2%
&nbsp;&nbsp;&nbsp;&nbsp;

🍎 APPLE ▲ 1.4%
&nbsp;&nbsp;&nbsp;&nbsp;

🪟 MICROSOFT ▲ 2.1%
&nbsp;&nbsp;&nbsp;&nbsp;

🏭 RELIANCE ▲ 0.8%
&nbsp;&nbsp;&nbsp;&nbsp;

💰 GOLD $2,425/oz
&nbsp;&nbsp;&nbsp;&nbsp;

₿ BITCOIN $108,450
&nbsp;&nbsp;&nbsp;&nbsp;

💵 USD/INR 83.42

</span>

</div>
"""

st.markdown(
    ticker_html,
    unsafe_allow_html=True
)

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

year = datetime.datetime.now().year

st.markdown(
f"""
<div class="footer">

<h4>X-Invo</h4>

<p>
Professional IPO Valuation &
Financial Intelligence Platform
</p>

<p>

Home |
IPO Predictor |
Markets |
News |
Learn |
Tools

</p>

<p>

© {year} X-Invo.
Built with Streamlit & Plotly.

</p>

</div>

""",
unsafe_allow_html=True
)

# ----------------------------------------------------------
# Sidebar Status
# ----------------------------------------------------------

st.sidebar.divider()

st.sidebar.success("🟢 System Online")

st.sidebar.metric(
    "Version",
    "1.0"
)

st.sidebar.metric(
    "Last Updated",
    datetime.datetime.now().strftime("%d %b %Y")
)

st.sidebar.metric(
    "Market Status",
    "OPEN"
)

st.sidebar.caption(
    "X-Invo Financial Intelligence Platform"
)
