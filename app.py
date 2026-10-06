import streamlit as st
import pandas as pd
from datetime import datetime

from src.visualization import (
    bubble_chart,
    choropleth_map,
    time_series_chart,
    stacked_area_chart,
    grouped_bar_chart,
    dual_axis_chart
)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CUSTOM CSS (Cleaned & Fixed)
# -------------------------------
st.markdown("""
<style>
    .main {
        background: #F4F7FE;
    }
    
    /* Dashboard Section Headings */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #FFFFFF !important; 
    }
    
    /* Section descriptions */
    .main p, .main .stMarkdown p {
        color: #CBD5E1 !important;
    }
    
    /* Streamlit headings */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: #F8FAFC !important;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: #1E3A8A;
    }
    section[data-testid="stSidebar"] * {
        color: white;
    }
    
    /* Standard Metrics */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 6px solid #2563EB;
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
    }
    div[data-testid="stMetric"] label {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800 !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* Filtered Summary Cards */
    .summary-card {
        background: #FFFFFF;
        border-left: 6px solid #2563EB;
        border-radius: 15px;
        padding: 22px 16px;
        min-height: 125px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: transform 0.2s ease;
    }
    .summary-card:hover {
        transform: translateY(-3px);
    }
    .summary-label {
        color: #374151;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 12px;
        white-space: nowrap;
    }
    .summary-value {
        color: #111827;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.1;
        white-space: nowrap;
    }
    .summary-small {
        font-size: 25px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 5px 5px 0px 0px;
        gap: 2px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data(show_spinner="Loading dataset...")
def load_data():
    return pd.read_csv("cleaned_data/googleplaystore_merged.csv")

df = load_data()

# -------------------------------
# FORMAT NUMBERS
# -------------------------------
def format_number(value):
    if value >= 1_000_000_000: return f"{value/1_000_000_000:.2f} B"
    elif value >= 1_000_000: return f"{value/1_000_000:.2f} M"
    elif value >= 1_000: return f"{value/1_000:.2f} K"
    else: return str(int(value))

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🎛 Dashboard Filters")

category = st.sidebar.multiselect("Category", sorted(df["Category"].dropna().unique()))
content_rating = st.sidebar.multiselect("Content Rating", sorted(df["Content Rating"].dropna().unique()))
app_type = st.sidebar.multiselect("App Type", sorted(df["Type"].dropna().unique()))
rating_filter = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=3.5, step=0.1)

# Apply Filters
with st.spinner('Applying filters...'):
    filtered_df = df.copy()
    if category: filtered_df = filtered_df[filtered_df["Category"].isin(category)]
    if content_rating: filtered_df = filtered_df[filtered_df["Content Rating"].isin(content_rating)]
    if app_type: filtered_df = filtered_df[filtered_df["Type"].isin(app_type)]
    filtered_df = filtered_df[filtered_df["Rating"] >= rating_filter]

# Download & Reset
st.sidebar.divider()
csv = filtered_df.to_csv(index=False)
st.sidebar.download_button("📥 Download Filtered CSV", csv, "Filtered_PlayStore_Data.csv", "text/csv")
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

# Raw Data Toggle
st.sidebar.divider()
show_raw_data = st.sidebar.checkbox("👀 Show Raw Data Table", value=False)

# -------------------------------
# MAIN HEADER
# -------------------------------
st.markdown(
    f"""
    <div style="background:linear-gradient(90deg,#2563EB,#1E40AF); padding:28px; border-radius:18px; margin-bottom:25px; text-align:center; color:white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color:white; margin:0; font-size:36px; font-weight: 800;">📊 Google Play Store Analytics Dashboard</h1>
        <h4 style="color:#E2E8F0; margin:8px 0; font-weight: 400;">Interactive Business Intelligence Dashboard</h4>
        <p style="color:#94A3B8; margin:0; font-size:13px; font-style: italic;">Last Updated: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}</p>
    </div>
    """, unsafe_allow_html=True
)

if show_raw_data:
    st.markdown("### 🗃️ Raw Data Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.divider()

# -------------------------------
# TAB NAVIGATION
# -------------------------------
tab_overview, tab_geo, tab_trends, tab_category = st.tabs([
    "📊 Overview & KPIs", 
    "🌍 Geography", 
    "📈 Time Trends", 
    "🧩 Category Deep-Dive"
])

# ==========================================
# TAB 1: OVERVIEW
# ==========================================
with tab_overview:
    
    # Global KPIs
    st.markdown("#### 🌐 Global Database Metrics (Unfiltered)")
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1: st.metric("📱 Total Apps", len(df))
    with kpi2: st.metric("⭐ Avg Rating", round(df["Rating"].mean(), 2))
    with kpi3: st.metric("📥 Total Installs", format_number(df["Installs"].sum()))
    with kpi4: st.metric("📝 Total Reviews", format_number(df["Reviews"].sum()))
    with kpi5: st.metric("💰 Paid Apps", len(df[df["Type"]=="Paid"]))
    with kpi6: st.metric("🆓 Free Apps", len(df[df["Type"]=="Free"]))
    
    st.divider()
    
    # Filtered Data Summary
    st.markdown("#### 🎯 Filtered Selection Performance")
    summary1, summary2, summary3, summary4, summary5 = st.columns([1, 1, 1.15, 1.15, 1])
    with summary1:
        st.markdown(f'<div class="summary-card"><div class="summary-label">📱 Selected Apps</div><div class="summary-value">{len(filtered_df):,}</div></div>', unsafe_allow_html=True)
    with summary2:
        f_rating = filtered_df["Rating"].mean() if not filtered_df.empty else 0
        st.markdown(f'<div class="summary-card"><div class="summary-label">⭐ Selected Avg Rating</div><div class="summary-value">{f_rating:.2f}</div></div>', unsafe_allow_html=True)
    with summary3:
        st.markdown(f'<div class="summary-card"><div class="summary-label">📥 Selected Installs</div><div class="summary-value summary-small">{format_number(filtered_df["Installs"].sum())}</div></div>', unsafe_allow_html=True)
    with summary4:
        st.markdown(f'<div class="summary-card"><div class="summary-label">📝 Selected Reviews</div><div class="summary-value summary-small">{format_number(filtered_df["Reviews"].sum())}</div></div>', unsafe_allow_html=True)
    with summary5:
        st.markdown(f'<div class="summary-card"><div class="summary-label">📂 Categories Included</div><div class="summary-value">{filtered_df["Category"].nunique()}</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bubble Chart
    with st.container(border=True):
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:5px;">
            <span style="font-size:26px;">📊</span>
            <span style="font-size:24px; font-weight:700; color:#FFFFFF;">Bubble Chart Analysis</span>
        </div>
        <p style="color:#CBD5E1; font-size:14px; margin-bottom:10px;">Relationship between App Size, Rating and Installs. Bubble size represents the number of installs.</p>
        """, unsafe_allow_html=True)
        
        figure = bubble_chart(filtered_df)
        if figure:
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": True, "responsive": True})
        else:
            st.warning("Bubble Chart is unavailable for the selected filters.")

# ==========================================
# TAB 2: GEOGRAPHY
# ==========================================
with tab_geo:
    
    st.markdown("#### 🏆 Top 5 Categories (by Installs)")
    top_category = filtered_df.groupby("Category")["Installs"].sum().sort_values(ascending=False).head(5).reset_index()
    if not top_category.empty:
        top_cols = st.columns(5)
        for i, row in top_category.iterrows():
            with top_cols[i]: st.metric(row["Category"], format_number(row["Installs"]))
    else:
        st.info("No category data available.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
        <div style="font-size:24px; font-weight:700; color:#FFFFFF; margin-bottom:5px;">🌍 Global Installs</div>
        <p style="color:#CBD5E1; font-size:14px;">Geographical distribution of app installs.</p>
        """, unsafe_allow_html=True)
        
        choropleth = choropleth_map(filtered_df)
        if choropleth:
            st.plotly_chart(choropleth, use_container_width=True, config={"displayModeBar": True, "responsive": True})
        else:
            st.info("A country field is not available in the current dataset, so a true geographical map cannot be generated.")

# ==========================================
# TAB 3: TRENDS
# ==========================================
with tab_trends:
    
    with st.container(border=True):
        st.markdown("""
        <div style="font-size:24px; font-weight:700; color:#FFFFFF; margin-bottom:5px;">📈 Time Series Analysis</div>
        <p style="color:#CBD5E1; font-size:14px;">Monthly application update trend based on Last Updated date.</p>
        """, unsafe_allow_html=True)
        
        ts_chart = time_series_chart(filtered_df)
        if ts_chart:
            st.plotly_chart(ts_chart, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        else:
            st.info("Time Series data is unavailable.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
        <div style="font-size:24px; font-weight:700; color:#FFFFFF; margin-bottom:5px;">🌊 Category Trend Over Time</div>
        <p style="color:#CBD5E1; font-size:14px;">Monthly installs across the top application categories.</p>
        """, unsafe_allow_html=True)
        
        stacked = stacked_area_chart(filtered_df)
        if stacked:
            st.plotly_chart(stacked, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        else:
            st.info("Stacked Area Chart unavailable.")

# ==========================================
# TAB 4: CATEGORY DEEP-DIVE
# ==========================================
with tab_category:
    
    st.markdown("#### 📊 Category Performance Breakdown")
    bar_col, dual_col = st.columns(2, gap="large")

    with bar_col:
        with st.container(border=True):
            st.markdown("<div style='font-size:20px; font-weight:600; color:#FFFFFF;'>📊 Apps & Reviews by Category</div>", unsafe_allow_html=True)
            grouped = grouped_bar_chart(filtered_df)
            if grouped:
                st.plotly_chart(grouped, use_container_width=True, config={"displayModeBar": False, "responsive": True})
            else:
                st.info("Grouped Bar Chart unavailable.")

    with dual_col:
        with st.container(border=True):
            st.markdown("<div style='font-size:20px; font-weight:600; color:#FFFFFF;'>📉 Installs vs Reviews</div>", unsafe_allow_html=True)
            dual = dual_axis_chart(filtered_df)
            if dual:
                st.plotly_chart(dual, use_container_width=True, config={"displayModeBar": False, "responsive": True})
            else:
                st.info("Dual Axis Chart unavailable.")