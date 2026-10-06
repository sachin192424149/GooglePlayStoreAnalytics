from datetime import datetime
import pytz
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def is_time_between(start_hour, end_hour):
    """
    Check whether current IST time is within the given range.
    """
    ist = pytz.timezone("Asia/Kolkata")
    current = datetime.now(ist).hour
    return start_hour <= current < end_hour


# =========================================================
# COMMON SETTINGS
# =========================================================

ALLOWED_CATEGORIES = [
    "GAME",
    "BEAUTY",
    "BUSINESS",
    "COMICS",
    "COMMUNICATION",
    "DATING",
    "ENTERTAINMENT",
    "SOCIAL",
    "EVENTS"
]

# =========================================================
# 1. PREPARE BUBBLE DATA
# =========================================================

def prepare_bubble_data(df):
    bubble = df.copy()

    if "Sentiment_Subjectivity" in bubble.columns:
        subjectivity = pd.to_numeric(
            bubble["Sentiment_Subjectivity"],
            errors="coerce"
        )
    else:
        subjectivity = pd.Series(1.0, index=bubble.index)

    bubble = bubble[
        (bubble["Rating"] > 3.5)
        & (bubble["Reviews"] > 500)
        & (bubble["Installs"] > 50000)
        & (subjectivity > 0.5)
        & (bubble["Category"].isin(ALLOWED_CATEGORIES))
        & (~bubble["App"].astype(str).str.contains("S", case=False, na=False))
    ].copy()

    return bubble

# =========================================================
# 2. HIGHLIGHT GAME
# =========================================================

def highlight_game(fig):
    for trace in fig.data:
        if str(trace.name).upper() == "GAME":
            trace.marker.color = "#FF1493"
            trace.marker.line.color = "#FFFFFF"
            trace.marker.line.width = 3
            trace.marker.opacity = 1
    return fig

# =========================================================
# 3. BUBBLE CHART
# =========================================================

def bubble_chart(df):
    bubble = prepare_bubble_data(df)

    if bubble.empty:
        return None

    fig = px.scatter(
        bubble,
        x="Size",
        y="Rating",
        size="Installs",
        color="Category",
        hover_name="App",
        hover_data={
            "Rating": ":.2f",
            "Reviews": ":,",
            "Installs": ":,",
            "Size": ":.1f",
        },
        size_max=45,
        opacity=0.75,
        title="App Size vs Average Rating"
    )

    fig = highlight_game(fig)

    fig.update_traces(
        marker=dict(
            line=dict(
                width=1.5,
                color="#FFFFFF"
            )
        )
    )

    # Indentation error fixed here
    fig.update_layout(
        template="plotly_dark",
        height=560,
        title={
            "text": "<b>App Size vs Average Rating</b>",
            "x": 0.5,
            "font": {
                "size": 24,
                "color": "#FFFFFF"
            }
        },
        xaxis=dict(
            title="App Size (MB)",
            title_font=dict(size=17, color="#FFFFFF"),
            tickfont=dict(size=14, color="#FFFFFF"),
            showgrid=True
        ),
        yaxis=dict(
            title="Average Rating",
            title_font=dict(size=17, color="#FFFFFF"),
            tickfont=dict(size=14, color="#FFFFFF"),
            range=[3.5, 5],
            showgrid=True
        ),
        legend_title="Category",
        margin=dict(l=65, r=35, t=75, b=55),
        hovermode="closest"
    )

    return fig

# =========================================================
# PREPARE CHOROPLETH DATA
# =========================================================

def prepare_choropleth_data(df):
    choropleth = df.copy()
    choropleth = choropleth[
        ~choropleth["Category"].astype(str).str.startswith(("A", "C", "G", "S"), na=False)
    ]
    choropleth = (
        choropleth
        .groupby("Category", as_index=False)["Installs"]
        .sum()
    )
    choropleth = choropleth.sort_values("Installs", ascending=False).head(5)

    countries = ["India", "United States", "Brazil", "Germany", "Australia"]
    choropleth["Country"] = countries[:len(choropleth)]
    choropleth["Highlight"] = (choropleth["Installs"] > 1_000_000)

    return choropleth

# =========================================================
# CHOROPLETH MAP
# =========================================================

def choropleth_map(df):
    choropleth = prepare_choropleth_data(df)

    if choropleth.empty:
        return None

    fig = px.choropleth(
        choropleth,
        locations="Country",
        locationmode="country names",
        color="Installs",
        hover_name="Category",
        hover_data={
            "Country": True,
            "Category": True,
            "Installs": ":,",
            "Highlight": True
        },
        color_continuous_scale="Viridis",
        title="🌍 Global Installs by Category"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        title={
            "text": "<b>🌍 Global Installs by Category</b>",
            "x": 0.5,
            "font": {
                "size": 25,
                "color": "#FFFFFF"
            }
        },
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#FFFFFF",
            showcountries=True,
            countrycolor="#666666",
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)"
        ),
        font=dict(color="#FFFFFF", size=15),
        margin=dict(l=20, r=20, t=80, b=20)
    )

    highlight = choropleth[choropleth["Highlight"] == True]

    if not highlight.empty:
        fig.add_scattergeo(
            locations=highlight["Country"],
            locationmode="country names",
            text=highlight["Category"],
            mode="markers+text",
            marker=dict(
                size=12,
                color="red",
                line=dict(color="#FFFFFF", width=1.5)
            ),
            textposition="top center",
            name="> 1 Million Installs"
        )

    return fig

# =========================================================
# 5. PREPARE DATE DATA
# =========================================================

def prepare_date_data(df):
    if "Last Updated" not in df.columns:
        return pd.DataFrame()
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Last Updated"], errors="coerce")
    data = data.dropna(subset=["Date"])
    return data

# =========================================================
# 6. TIME SERIES CHART
# =========================================================

def time_series_chart(df):
    data = prepare_date_data(df)

    if data.empty:
        return None

    monthly = (
        data
        .groupby(data["Date"].dt.to_period("M"))
        .agg(Apps=("App", "count"), Installs=("Installs", "sum"))
        .reset_index()
    )
    monthly["Date"] = monthly["Date"].dt.to_timestamp()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["Date"],
            y=monthly["Apps"],
            mode="lines+markers",
            name="Apps Updated",
            line=dict(width=3),
            marker=dict(size=7)
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=550,
        title={
            "text": "<b>Monthly App Update Trend</b>",
            "x": 0.5,
            "font": {"size": 24, "color": "#FFFFFF"}
        },
        xaxis=dict(
            title="Month",
            tickfont=dict(size=13, color="#FFFFFF"),
            title_font=dict(color="#FFFFFF")
        ),
        yaxis=dict(
            title="Number of Apps",
            tickfont=dict(size=13, color="#FFFFFF"),
            title_font=dict(color="#FFFFFF")
        ),
        hovermode="x unified",
        margin=dict(l=60, r=30, t=90, b=60)
    )

    return fig

# =========================================================
# 7. STACKED AREA CHART
# =========================================================

def stacked_area_chart(df):
    data = prepare_date_data(df)

    if data.empty:
        return None

    top_categories = (
        data
        .groupby("Category")["Installs"]
        .sum()
        .nlargest(5)
        .index
    )

    data = data[data["Category"].isin(top_categories)].copy()

    monthly = (
        data
        .groupby([data["Date"].dt.to_period("M"), "Category"])["Installs"]
        .sum()
        .reset_index()
    )
    monthly["Date"] = monthly["Date"].dt.to_timestamp()

    fig = px.area(
        monthly,
        x="Date",
        y="Installs",
        color="Category",
        title="Monthly Installs by Top Categories"
    )

    fig.update_layout(
        template="plotly_dark",
        height=550,
        title={
            "x": 0.5,
            "font": {"size": 24, "color": "#FFFFFF"}
        },
        xaxis_title="Month",
        yaxis_title="Installs",
        hovermode="x unified",
        margin=dict(l=60, r=30, t=90, b=60)
    )

    return fig

# =========================================================
# GROUPED BAR CHART
# =========================================================

def grouped_bar_chart(df):
    if df.empty:
        return None

    g = (
        df.groupby("Category")
        .agg(Apps=("App", "count"), Reviews=("Reviews", "sum"))
        .reset_index()
    )
    g = g.sort_values("Apps", ascending=False).head(10)

    fig = px.bar(
        g,
        x="Category",
        y=["Apps", "Reviews"],
        barmode="group",
        title="Top Categories: Apps and Reviews"
    )

    fig.update_layout(
        template="plotly_dark",
        height=480,
        title_x=0.5,
        xaxis_tickangle=-35,
        margin=dict(l=45, r=20, t=70, b=100)
    )

    return fig

# =========================================================
# DUAL AXIS CHART
# =========================================================

def dual_axis_chart(df):
    if df.empty:
        return None

    category_data = (
        df.groupby("Category")
        .agg(Installs=("Installs", "sum"), Reviews=("Reviews", "sum"))
        .reset_index()
    )
    category_data = category_data.sort_values("Installs", ascending=False).head(10)

    if category_data.empty:
        return None

    fig = go.Figure()

    # Installs
    fig.add_trace(
        go.Bar(
            x=category_data["Category"],
            y=category_data["Installs"],
            name="Installs",
            marker=dict(
                color="#4F46E5",
                line=dict(width=0)
            ),
            hovertemplate="<b>%{x}</b><br>Installs: %{y:,}<extra></extra>"
        )
    )

    # Reviews
    fig.add_trace(
        go.Scatter(
            x=category_data["Category"],
            y=category_data["Reviews"],
            name="Reviews",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#F97316", width=4),
            marker=dict(
                size=9,
                color="#F97316",
                line=dict(color="white", width=2)
            ),
            hovertemplate="<b>%{x}</b><br>Reviews: %{y:,}<extra></extra>"
        )
    )

    # Layout
    fig.update_layout(
        template="plotly_dark",
        height=560,
        title={
            "text": "<b>Installs vs Reviews by Category</b>",
            "x": 0.5,
            "font": {"size": 23, "color": "#FFFFFF"}
        },
        xaxis=dict(
            title="Category",
            tickangle=-30,
            tickfont=dict(size=12, color="#FFFFFF"),
            title_font=dict(color="#FFFFFF"),
            showgrid=False
        ),
        yaxis=dict(
            title="Total Installs",
            tickfont=dict(size=12, color="#FFFFFF"),
            title_font=dict(color="#FFFFFF"),
            gridcolor="#4B5563",
            showgrid=True
        ),
        yaxis2=dict(
            title="Total Reviews",
            overlaying="y",
            side="right",
            tickfont=dict(size=12, color="#FFFFFF"),
            title_font=dict(color="#FFFFFF")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
        margin=dict(l=65, r=75, t=100, b=100)
    )

    return fig