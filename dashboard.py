
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="India Unemployment Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. PROFESSIONAL DASHBOARD CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #090D27,
        #171B46,
        #111A3D
    );
    color: white;
}

.block-container {
    max-width: 1800px;
    padding: 1.5rem 2rem 2rem 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Dashboard title */

.dashboard-header {
    background: linear-gradient(
        100deg,
        #401D43,
        #18274D
    );
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #65729A;
    margin-bottom: 20px;
}

.dashboard-title {
    color: white;
    font-size: 29px;
    font-weight: 800;
    margin: 0;
}

.dashboard-subtitle {
    color: #C5D0E8;
    font-size: 13px;
    margin-top: 8px;
}

/* Filters */

div[data-testid="stSelectbox"] label {
    color: white !important;
    font-weight: 700;
}

/* KPI cards */

div[data-testid="stMetric"] {
    background: #192951;
    border: 1px solid #6579A8;
    padding: 18px;
    border-radius: 12px;
    min-height: 110px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

div[data-testid="stMetricLabel"] {
    color: #D5DDF0 !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 800;
}

/* Headings */

h1, h2, h3 {
    color: white !important;
}

/* Chart panels */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #52658E !important;
    border-radius: 10px;
}

/* Divider */

hr {
    border-color: #52658E;
    margin-top: 25px;
    margin-bottom: 25px;
}

/* Download button */

.stDownloadButton button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 700;
    padding: 10px 18px;
}

.stDownloadButton button:hover {
    background-color: #1D4ED8;
    color: white;
}

/* Footer */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = "outputs/cleaned_unemployment_india.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Estimated Unemployment Rate (%)",
        "Estimated Employed",
        "Estimated Labour Participation Rate (%)"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df["Region"] = df["Region"].astype(str).str.strip()

    df["Area"] = (
        df["Area"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df.dropna(
        subset=[
            "Date",
            "Region",
            "Area",
            "Estimated Unemployment Rate (%)",
            "Estimated Employed",
            "Estimated Labour Participation Rate (%)"
        ],
        inplace=True
    )

    return df


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Cleaned dataset not found. "
        "Please run main.py first."
    )

    st.stop()


RATE = "Estimated Unemployment Rate (%)"
EMPLOYED = "Estimated Employed"
PARTICIPATION = "Estimated Labour Participation Rate (%)"



# =========================================================
# 4. DASHBOARD HEADER
# =========================================================

st.html("""
<div style="
    background: linear-gradient(100deg, #401D43, #18274D);
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #65729A;
    margin-bottom: 20px;
">
    <h1 style="
        color: white;
        font-size: 29px;
        font-weight: 800;
        margin: 0;
    ">
        📊 UNEMPLOYMENT ANALYSIS DURING COVID-19 IN INDIA
    </h1>

    <p style="
        color: #C5D0E8;
        font-size: 13px;
        margin-top: 8px;
    ">
        DATA ANALYTICS DASHBOARD |
        EMPLOYMENT TRENDS |
        REGIONAL COMPARISON |
        COVID-19 IMPACT
    </p>
</div>
""")


# =========================================================
# 5. INTERACTIVE FILTERS
# =========================================================

filter1, filter2, filter3 = st.columns(3)

with filter1:

    state_options = (
        ["All"] +
        sorted(df["Region"].dropna().unique().tolist())
    )

    selected_state = st.selectbox(
        "SELECT STATE",
        state_options
    )


with filter2:

    date_values = sorted(
        df["Date"].dt.strftime("%Y-%m-%d").unique()
    )

    date_options = ["All"] + date_values

    selected_date = st.selectbox(
        "SELECT DATE",
        date_options
    )


with filter3:

    area_options = (
        ["All"] +
        sorted(df["Area"].dropna().unique().tolist())
    )

    selected_area = st.selectbox(
        "SELECT AREA",
        area_options
    )


# Apply filters

filtered_df = df.copy()

if selected_state != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_state
    ]


if selected_date != "All":

    filtered_df = filtered_df[
        filtered_df["Date"].dt.strftime("%Y-%m-%d")
        == selected_date
    ]


if selected_area != "All":

    filtered_df = filtered_df[
        filtered_df["Area"] == selected_area
    ]


if filtered_df.empty:

    st.warning(
        "No data available for the selected filters. "
        "Please change your filter selections."
    )

    st.stop()


# =========================================================
# 6. KEY PERFORMANCE INDICATORS
# =========================================================

st.markdown("### KEY PERFORMANCE INDICATORS")

k1, k2, k3, k4 = st.columns(4)

average_unemployment = filtered_df[RATE].mean()

average_employed = filtered_df[EMPLOYED].mean() / 1_000_000

average_participation = filtered_df[PARTICIPATION].mean()

states_count = filtered_df["Region"].nunique()


k1.metric(
    "Average Unemployment",
    f"{average_unemployment:.2f}%"
)

k2.metric(
    "Average Employed",
    f"{average_employed:.2f}M"
)

k3.metric(
    "Labour Participation",
    f"{average_participation:.2f}%"
)

k4.metric(
    "States Analysed",
    states_count
)


st.divider()


# =========================================================
# 7. COMMON PROFESSIONAL CHART STYLE
# =========================================================

def style_chart(fig, height=340):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial",
            size=11,
            color="#FFFFFF"
        ),

        height=height,

        margin=dict(
            l=55,
            r=85,
            t=55,
            b=50
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),

        hoverlabel=dict(
            bgcolor="#17264A",
            font_color="white"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        automargin=True
    )

    fig.update_yaxes(
        gridcolor="rgba(180,195,230,0.15)",
        zeroline=False,
        automargin=True
    )

    return fig


# =========================================================
# 8. CHART 1 - MONTHLY UNEMPLOYMENT TREND
# =========================================================

monthly_data = (

    filtered_df.groupby("Date")[RATE]

    .mean()

    .reset_index()

    .sort_values("Date")

)

fig1 = px.area(

    monthly_data,

    x="Date",

    y=RATE,

    title="Unemployment Rate by Year and Month",

    color_discrete_sequence=["#16D9F5"]

)

fig1.update_traces(

    line=dict(width=3),

    fillcolor="rgba(22,217,245,0.30)"

)

fig1.update_layout(

    yaxis_title="Unemployment Rate (%)",

    xaxis_title="Date"

)

fig1 = style_chart(fig1, 340)


# =========================================================
# 9. CHART 2 - UNEMPLOYMENT RATE BY AREA
# =========================================================

area_data = (

    filtered_df.groupby("Area")[RATE]

    .mean()

    .reset_index()

)

fig2 = px.pie(

    area_data,

    names="Area",

    values=RATE,

    hole=0.58,

    title="Unemployment Rate by Area",

    color="Area",

    color_discrete_map={

        "Urban": "#E9C229",

        "Rural": "#FFF000"

    }

)

fig2.update_traces(

    textposition="outside",

    textinfo="percent+label",

    marker=dict(
        line=dict(
            color="#17204A",
            width=2
        )
    )

)

fig2 = style_chart(fig2, 340)


# =========================================================
# 10. CHART 3 - AVERAGE EMPLOYED BY STATES
# =========================================================

state_employed = (

    filtered_df.groupby("Region")[EMPLOYED]

    .mean()

    .reset_index()

    .sort_values(EMPLOYED, ascending=False)

    .head(15)

)

state_employed["Employed_Millions"] = (

    state_employed[EMPLOYED] / 1_000_000

)


fig3 = px.bar(

    state_employed.sort_values("Employed_Millions"),

    x="Employed_Millions",

    y="Region",

    orientation="h",

    text="Employed_Millions",

    title="Average Employed by States",

    color_discrete_sequence=["#00E83A"]

)

fig3.update_traces(

    texttemplate="%{text:.2f}M",

    textposition="outside",

    cliponaxis=False

)

fig3.update_layout(

    xaxis_title="Average Employed (Millions)",

    yaxis_title="State"

)

fig3 = style_chart(fig3, 340)


# =========================================================
# 11. CHART 4 - UNEMPLOYMENT RATE BY STATES
# =========================================================

state_unemployment = (

    filtered_df.groupby("Region")[RATE]

    .mean()

    .reset_index()

    .sort_values(RATE, ascending=False)

    .head(15)

)

fig4 = px.bar(

    state_unemployment.sort_values(RATE),

    x=RATE,

    y="Region",

    orientation="h",

    text=RATE,

    title="Average Unemployment Rate by States",

    color_discrete_sequence=["#FF2525"]

)

fig4.update_traces(

    texttemplate="%{text:.2f}%",

    textposition="outside",

    cliponaxis=False

)

fig4.update_layout(

    xaxis_title="Unemployment Rate (%)",

    yaxis_title="State"

)

fig4 = style_chart(fig4, 340)


# =========================================================
# 12. CHART 5 - AVERAGE EMPLOYED BY AREA
# =========================================================

area_employed = (

    filtered_df.groupby("Area")[EMPLOYED]

    .mean()

    .reset_index()

)

fig5 = px.pie(

    area_employed,

    names="Area",

    values=EMPLOYED,

    hole=0.58,

    title="Average Employed by Area",

    color="Area",

    color_discrete_map={

        "Rural": "#13E68A",

        "Urban": "#168BFF"

    }

)

fig5.update_traces(

    textposition="outside",

    textinfo="percent+label",

    marker=dict(
        line=dict(
            color="#17204A",
            width=2
        )
    )

)

fig5 = style_chart(fig5, 340)


# =========================================================
# 13. CHART 6 - TOP 5 LABOUR PARTICIPATION STATES
# =========================================================

labour_data = (

    filtered_df.groupby("Region")[PARTICIPATION]

    .mean()

    .reset_index()

    .sort_values(PARTICIPATION, ascending=False)

    .head(5)

    .sort_values(PARTICIPATION)

)

fig6 = px.bar(

    labour_data,

    x=PARTICIPATION,

    y="Region",

    orientation="h",

    text=PARTICIPATION,

    title="Top 5 Labour Participation States",

    color_discrete_sequence=["#FFA500"]

)

fig6.update_traces(

    texttemplate="%{text:.2f}%",

    textposition="outside",

    cliponaxis=False

)

fig6.update_layout(

    xaxis_title="Labour Participation Rate (%)",

    yaxis_title="State"

)

fig6 = style_chart(fig6, 340)


# =========================================================
# 14. SIX-PANEL DASHBOARD LAYOUT
# =========================================================

st.markdown(
    "### 📊 UNEMPLOYMENT ANALYTICS OVERVIEW"
)


# ---------------- ROW 1 ----------------

col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):

        st.markdown(
            "<div style='text-align:center;"
            "font-weight:bold;color:white;'>"
            "UNEMPLOYMENT RATE BY YEAR AND MONTH"
            "</div>",
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col2:

    with st.container(border=True):

        st.markdown(
            "<div style='text-align:center;"
            "font-weight:bold;color:white;'>"
            "UNEMPLOYMENT RATE BY AREA"
            "</div>",
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col3:

    with st.container(border=True):

        st.markdown(
            "<div style='text-align:center;"
            "font-weight:bold;color:white;'>"
            "AVERAGE EMPLOYED BY STATES"
            "</div>",
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# ---------------- ROW 2 ----------------

col4, col5, col6 = st.columns(3)


with col4:

    with st.container(border=True):

        st.markdown(
            "<div style='text-align:center;"
            "font-weight:bold;color:white;'>"
            "AVERAGE UNEMPLOYMENT RATE BY STATES"
            "</div>",
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig4,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col5:

    with st.container(border=True):

        st.markdown(
            "<div style='text-align:center;"
            "font-weight:bold;color:white;'>"
            "AVERAGE EMPLOYED BY AREA"
            "</div>",
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig5,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col6:

    with st.container(border=True):

        st.markdown(
            "<div style='text-align:center;"
            "font-weight:bold;color:white;'>"
            "TOP 5 LABOUR PARTICIPATION STATES"
            "</div>",
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig6,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# =========================================================
# 15. DATA TABLE AND DOWNLOAD
# =========================================================

st.divider()

st.markdown("### 📋 DETAILED UNEMPLOYMENT DATA")

with st.expander("View filtered dataset"):

    st.dataframe(

        filtered_df,

        use_container_width=True,

        hide_index=True

    )


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="⬇️ Download Filtered Dataset",

    data=csv_data,

    file_name="india_unemployment_analysis.csv",

    mime="text/csv"

)



# =========================================================
# 16. PROFESSIONAL FOOTER
# =========================================================

st.divider()

st.html("""
<div style="
    background: linear-gradient(100deg, #18254A, #29204B);
    border: 1px solid #6579A8;
    border-radius: 12px;
    padding: 28px;
    text-align: center;
">

    <h3 style="color: white; margin-bottom: 8px;">
        📊 INDIA UNEMPLOYMENT ANALYTICS
    </h3>

    <p style="color: #C5D0E8;">
        Transforming employment data into meaningful insights
    </p>

    <p style="color: white;">
        Python | Streamlit | Pandas | Plotly
    </p>

    <p style="color: #AFC1E8;">
        CodeAlpha Data Science Internship | Task 2
    </p>

    <p style="color: #8EA3CE; font-size: 12px;">
        Data source: Provided unemployment datasets
    </p>

</div>
""")
