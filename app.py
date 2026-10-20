import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Marketing Performance Dashboard", page_icon="📊", layout="wide")


# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def summarize(data, group_col):
    """Totals per group, with KPIs recalculated from the totals."""
    g = data.groupby(group_col).agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
    )
    g["ctr"] = g["clicks"] / g["impressions"] * 100
    g["conversion_rate"] = g["conversions"] / g["clicks"] * 100
    g["roas"] = g["revenue"] / g["spend"]
    g["roi"] = (g["revenue"] - g["spend"]) / g["spend"] * 100
    return g.reset_index()


df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")
min_d, max_d = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
channels = st.sidebar.multiselect("Channel", sorted(df["channel"].unique()), default=sorted(df["channel"].unique()))
campaigns = st.sidebar.multiselect("Campaign", sorted(df["campaign_name"].unique()), default=sorted(df["campaign_name"].unique()))
audiences = st.sidebar.multiselect("Target audience", sorted(df["target_audience"].unique()), default=sorted(df["target_audience"].unique()))

if len(date_range) != 2:
    st.info("Please pick both a start and an end date.")
    st.stop()

mask = (
    (df["date"].dt.date >= date_range[0])
    & (df["date"].dt.date <= date_range[1])
    & df["channel"].isin(channels)
    & df["campaign_name"].isin(campaigns)
    & df["target_audience"].isin(audiences)
)
f = df[mask]

if f.empty:
    st.warning("No data for these filters. Please widen your selection.")
    st.stop()

# ---------- HEADER + KPI CARDS ----------
st.title("📊 Marketing Performance Dashboard")
st.caption("Blinkit marketing campaigns, Mar 2023 to Nov 2024")

total = summarize(f.assign(all="Total"), "all").iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric("Total Spend", f"₹{total['spend']:,.0f}")
c2.metric("Total Revenue", f"₹{total['revenue']:,.0f}")
c3.metric("ROI", f"{total['roi']:.1f}%")
c4, c5, c6 = st.columns(3)
c4.metric("CTR", f"{total['ctr']:.2f}%")
c5.metric("Conversion Rate", f"{total['conversion_rate']:.2f}%")
c6.metric("ROAS", f"{total['roas']:.2f}x")

st.divider()

# ---------- CHANNEL COMPARISON ----------
by_channel = summarize(f, "channel").sort_values("roi", ascending=False)
by_campaign = summarize(f, "campaign_name").sort_values("roi", ascending=False)
by_audience = summarize(f, "target_audience").sort_values("conversion_rate", ascending=False)

left, right = st.columns(2)
with left:
    st.subheader("Channel comparison: ROI (%)")
    fig = px.bar(by_channel, x="channel", y="roi", text=by_channel["roi"].round(1), color="channel")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="ROI (%)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Channel comparison: CTR vs Conversion rate (%)")
    melted = by_channel.melt(id_vars="channel", value_vars=["ctr", "conversion_rate"], var_name="metric", value_name="value")
    fig = px.bar(melted, x="channel", y="value", color="metric", barmode="group")
    fig.update_layout(xaxis_title="", yaxis_title="%")
    st.plotly_chart(fig, use_container_width=True)

# ---------- CAMPAIGN PERFORMANCE ----------
st.subheader("Campaign performance: ROI (%)")
fig = px.bar(by_campaign, x="roi", y="campaign_name", orientation="h", text=by_campaign["roi"].round(1))
fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="ROI (%)", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

# ---------- TRENDS ----------
st.subheader("Monthly trends")
monthly = summarize(f, "month").sort_values("month")
if "2024-11" in monthly["month"].values:
    st.caption("Note: Nov 2024 is a partial month (data only up to 5 Nov), so its totals look low.")

t1, t2 = st.columns(2)
with t1:
    fig = px.line(monthly, x="month", y=["spend", "revenue"], markers=True)
    fig.update_layout(xaxis_title="", yaxis_title="Amount (₹)", legend_title="")
    st.plotly_chart(fig, use_container_width=True)
with t2:
    fig = px.line(monthly, x="month", y=["ctr", "conversion_rate"], markers=True)
    fig.update_layout(xaxis_title="", yaxis_title="%", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

# ---------- AUDIENCE ----------
st.subheader("Conversion rate by target audience (%)")
fig = px.bar(by_audience, x="target_audience", y="conversion_rate", text=by_audience["conversion_rate"].round(2))
fig.update_layout(xaxis_title="", yaxis_title="Conversion rate (%)")
st.plotly_chart(fig, use_container_width=True)

# ---------- BUSINESS INSIGHTS ----------
st.divider()
st.subheader("💡 Business insights (based on current filters)")
best_ch, worst_ch = by_channel.iloc[0], by_channel.iloc[-1]
best_cp, worst_cp = by_campaign.iloc[0], by_campaign.iloc[-1]
best_conv = by_channel.sort_values("conversion_rate", ascending=False).iloc[0]
st.markdown(
    f"""
- **Best channel by ROI:** {best_ch['channel']} ({best_ch['roi']:.1f}%). Weakest: {worst_ch['channel']} ({worst_ch['roi']:.1f}%).
- **Highest conversion rate:** {best_conv['channel']} ({best_conv['conversion_rate']:.2f}%).
- **Best campaign by ROI:** {best_cp['campaign_name']} ({best_cp['roi']:.1f}%). Weakest: {worst_cp['campaign_name']} ({worst_cp['roi']:.1f}%).
- **Suggestion:** shift part of the budget from the weakest channel and campaign towards the best ones, and test the change.
- **Caution:** differences between groups are small, so treat them as hints, not firm conclusions.
"""
)

# ---------- DATA + REPORT DOWNLOAD ----------
with st.expander("View filtered data"):
    st.dataframe(f, use_container_width=True)

st.download_button("⬇️ Download campaign summary report (CSV)", by_campaign.round(2).to_csv(index=False), "campaign_report.csv", "text/csv")
st.download_button("⬇️ Download channel summary report (CSV)", by_channel.round(2).to_csv(index=False), "channel_report.csv", "text/csv")
