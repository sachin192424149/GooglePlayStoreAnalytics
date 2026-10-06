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
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>

.main{
    background:#F4F7FE;
}
/* =====================================================
   DASHBOARD SECTION HEADINGS
   ===================================================== */

.main h1,
.main h2,
.main h3,
.main h4,
.main h5,
.main h6 {
    color:#FFFFFF;!important;
}

/* Section descriptions */
.main p,
.main .stMarkdown p {
    color:#CBD5E1 !important;
}

/* Streamlit headings */
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    color:#F8FAFC !important;
}   w

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

section[data-testid="stSidebar"]{
    background:#1E3A8A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

div[data-testid="stMetric"] {
    background:#FFFFFF !important;
    border-radius:15px;
    padding:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.25);
    text-align:center;
    border-left:6px solid #2563EB;
}

/* KPI label */
div[data-testid="stMetric"] label {
    color:#374151 !important;
    font-weight:600 !important;
}

/* KPI value */
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color:#111827 !important;
    font-weight:800 !important;
}

/* KPI delta if present */
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color:#374151 !important;
}

.stButton>button{

    width:100%;

    border-radius:10px;

}

/* Filtered Summary Cards */

.summary-card {
    background:#FFFFFF;
    border-left:6px solid #2563EB;
    border-radius:15px;
    padding:22px 16px;
    min-height:125px;
    text-align:center;
    box-shadow:0 5px 15px rgba(0,0,0,0.20);
    overflow:hidden;
}

.summary-label {
    color:#374151;
    font-size:16px;
    font-weight:600;
    margin-bottom:12px;
    white-space:nowrap;
}

.summary-value {
    color:#FFFFFF;
    font-size:32px;
    font-weight:800;
    line-height:1.1;
    white-space:nowrap;
}

.summary-small {
    font-size:25px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(
        "cleaned_data/googleplaystore_merged.csv"
    )

df = load_data()

# -------------------------------
# HEADER
# -------------------------------

st.markdown(
    f"""
<div style="background:linear-gradient(90deg,#2563EB,#1E40AF);
            padding:28px;
            border-radius:18px;
            margin-bottom:25px;
            text-align:center;
            color:white;">

<h1 style="color:white;margin:0;font-size:34px;">
📊 Google Play Store Analytics Dashboard
</h1>

<h4 style="color:white;margin:8px 0;">
Interactive Business Intelligence Dashboard
</h4>

<p style="color:white;margin:0;font-size:14px;">
Last Updated: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}
</p>

</div>
""",
    unsafe_allow_html=True
)

# -------------------------------
# FORMAT NUMBERS
# -------------------------------

def format_number(value):

    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f} B"

    elif value >= 1_000_000:
        return f"{value/1_000_000:.2f} M"

    elif value >= 1_000:
        return f"{value/1_000:.2f} K"

    else:
        return str(int(value))

# -------------------------------
# KPI VALUES
# -------------------------------

total_apps = len(df)

avg_rating = round(df["Rating"].mean(),2)

total_installs = format_number(
    df["Installs"].sum()
)

total_reviews = format_number(
    df["Reviews"].sum()
)

paid_apps = len(
    df[df["Type"]=="Paid"]
)

free_apps = len(
    df[df["Type"]=="Free"]
)

# -------------------------------
# KPI ROW 1
# -------------------------------

kpi1,kpi2,kpi3 = st.columns(3)

with kpi1:

    st.metric(
        "📱 Total Apps",
        total_apps
    )

with kpi2:

    st.metric(
        "⭐ Average Rating",
        avg_rating
    )

with kpi3:

    st.metric(
        "📥 Total Installs",
        total_installs
    )

# -------------------------------
# KPI ROW 2
# -------------------------------

kpi4,kpi5,kpi6 = st.columns(3)

with kpi4:

    st.metric(
        "📝 Total Reviews",
        total_reviews
    )

with kpi5:

    st.metric(
        "💰 Paid Apps",
        paid_apps
    )

with kpi6:

    st.metric(
        "🆓 Free Apps",
        free_apps
    )

st.divider()

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.header("🎛 Dashboard Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].dropna().unique())
)

content_rating = st.sidebar.multiselect(
    "Content Rating",
    sorted(df["Content Rating"].dropna().unique())
)

app_type = st.sidebar.multiselect(
    "App Type",
    sorted(df["Type"].dropna().unique())
)

rating_filter = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=3.5,
    step=0.1
)

filtered_df = df.copy()

if category:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category)
    ]

if content_rating:
    filtered_df = filtered_df[
        filtered_df["Content Rating"].isin(content_rating)
    ]

if app_type:
    filtered_df = filtered_df[
        filtered_df["Type"].isin(app_type)
    ]

filtered_df = filtered_df[
    filtered_df["Rating"] >= rating_filter
]

csv = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    "📥 Download CSV",
    csv,
    "Filtered_PlayStore_Data.csv",
    "text/csv",
    use_container_width=True
)

if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):
    st.rerun()

# -------------------------------
# BUBBLE CHART
# -------------------------------

with st.container(border=True):

    st.markdown("""
    <div style="
        display:flex;
        align-items:center;
        gap:12px;
        margin-bottom:5px;
    ">
        <span style="font-size:30px;">📊</span>
        <span style="
            font-size:28px;
            font-weight:700;
            color:#FFFFFF;
        ">
            Bubble Chart Analysis
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style="
            color:#64748B;
            font-size:15px;
            margin-bottom:10px;
        ">
        Relationship between App Size, Rating and Installs.
        Bubble size represents the number of installs.
        </p>
        """,
        unsafe_allow_html=True
    )

    figure = bubble_chart(filtered_df)

    if figure is not None:

        st.plotly_chart(
            figure,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "responsive": True
            }
        )

    else:

        st.warning(
            "Bubble Chart is unavailable for the selected filters."
        )


st.divider()

# ==========================================
# FILTERED SUMMARY
# ==========================================

st.markdown("## 📈 Filtered Data Summary")

st.caption(
    "Key statistics based on the filters currently selected."
)

summary1, summary2, summary3, summary4, summary5 = st.columns(
    [1, 1, 1.15, 1.15, 1]
)

with summary1:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">📱 Apps</div>
            <div class="summary-value">
                {len(filtered_df):,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with summary2:

    filtered_rating = (
        filtered_df["Rating"].mean()
        if len(filtered_df) > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">⭐ Avg Rating</div>
            <div class="summary-value">
                {filtered_rating:.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with summary3:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">📥 Installs</div>
            <div class="summary-value summary-small">
                {format_number(filtered_df["Installs"].sum())}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with summary4:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">📝 Reviews</div>
            <div class="summary-value summary-small">
                {format_number(filtered_df["Reviews"].sum())}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with summary5:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">📂 Categories</div>
            <div class="summary-value">
                {filtered_df["Category"].nunique()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


# ==========================================
# CHOROPLETH MAP
# ==========================================

with st.container(border=True):

    st.markdown("""
    <div style="
        font-size:28px;
        font-weight:700;
        color:#FFFFFF;
        margin-bottom:5px;
    ">
        🌍 Global Installs
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Geographical distribution of app installs."
    )

    choropleth = choropleth_map(
        filtered_df
    )

    if choropleth is not None:

        st.plotly_chart(
            choropleth,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "responsive": True
            }
        )

    else:

        st.info(
            "A country field is not available in the current dataset, "
            "so a true geographical map cannot be generated."
        )


# ==========================================
# TOP CATEGORIES
# ==========================================

st.markdown("## 🏆 Top Categories")

st.caption(
    "Top 5 categories based on total installs."
)

top_category = (
    filtered_df
    .groupby("Category")["Installs"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

if not top_category.empty:

    top_cols = st.columns(5)

    for i, row in top_category.iterrows():

        with top_cols[i]:

            st.metric(
                row["Category"],
                format_number(
                    row["Installs"]
                )
            )

else:

    st.info(
        "No category data available."
    )


st.divider()


# ==========================================
# TIME SERIES
# ==========================================

with st.container(border=True):

    st.markdown("""
    <div style="
        font-size:28px;
        font-weight:700;
        color:#FFFFFF;
        margin-bottom:5px;
    ">
        📈 Time Series Analysis
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Monthly application update trend based on Last Updated."
    )

    ts_chart = time_series_chart(
        filtered_df
    )

    if ts_chart is not None:

        st.plotly_chart(
            ts_chart,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            }
        )

    else:

        st.info(
            "Time Series data is unavailable."
        )


st.divider()


# ==========================================
# CATEGORY ANALYSIS
# ==========================================

st.markdown("## 📊 Category Performance")

bar_col, dual_col = st.columns(
    2,
    gap="large"
)


# ------------------------------------------
# GROUPED BAR
# ------------------------------------------

with bar_col:

    with st.container(border=True):

        st.markdown("### 📊 Apps & Reviews")

        grouped = grouped_bar_chart(
            filtered_df
        )

        if grouped is not None:

            st.plotly_chart(
                grouped,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
            )

        else:

            st.info(
                "Grouped Bar Chart unavailable."
            )


# ------------------------------------------
# DUAL AXIS
# ------------------------------------------

with dual_col:

    with st.container(border=True):

        st.markdown(
            "### 📉 Installs vs Reviews"
        )

        dual = dual_axis_chart(
            filtered_df
        )

        if dual is not None:

            st.plotly_chart(
                dual,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
            )

        else:

            st.info(
                "Dual Axis Chart unavailable."
            )


st.divider()


# ==========================================
# STACKED AREA
# ==========================================

with st.container(border=True):

    st.markdown("""
    <div style="
        font-size:28px;
        font-weight:700;
        color:#FFFFFF;
        margin-bottom:5px;
    ">
        🌊 Category Trend
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Monthly installs across the top application categories."
    )

    stacked = stacked_area_chart(
        filtered_df
    )

    if stacked is not None:

        st.plotly_chart(
            stacked,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            }
        )

    else:

        st.info(
            "Stacked Area Chart unavailable."
        )


st.divider()