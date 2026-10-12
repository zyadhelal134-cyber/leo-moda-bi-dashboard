import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="El-Sharnouby | Business Intelligence",
                   page_icon="📊", layout="wide")

BLUE = "#2878E3"
GREEN = "#16A879"
LIGHT_BLUE = "#B8D4F5"
GRID = "#E8EDF3"

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
  background: white; border: 1px solid #e3e8ef;
  padding: 14px 16px; border-radius: 12px;
}
[data-testid="stMetricLabel"] {color:#475569; font-size:.9rem;}
[data-testid="stMetricValue"] {color:#111827; font-size:1.75rem;}
</style>
""", unsafe_allow_html=True)

st.title("🎯 El-Sharnouby | Executive Command Center")
st.caption("Interactive dashboard • Upload your real business data to begin")

with st.sidebar:
    st.header("Data & Filters")
    uploaded = st.file_uploader("Upload sales data (CSV or Excel)", type=["csv", "xlsx", "xls"])
    st.caption("Your file should contain one row per sale/order/item, with columns such as date, sales, profit, channel, or branch.")

if uploaded is None:
    st.info("Upload your real CSV/Excel file using the sidebar. The dashboard will build charts from that file; it does not generate fake business figures.")
    st.markdown("""
### Suggested data columns
- **Date** — order or invoice date
- **Net Sales** — sales value after returns/discounts, if available
- **Gross Profit** — gross profit amount, if available
- **Channel** — store / online, if available
- **Branch** — branch or location, if available
- **Discount** and **Quality Cost** — optional
    """)
    st.stop()

try:
    if uploaded.name.lower().endswith(".csv"):
        try:
            raw = pd.read_csv(uploaded)
        except UnicodeDecodeError:
            uploaded.seek(0)
            raw = pd.read_csv(uploaded, encoding="latin-1")
    else:
        raw = pd.read_excel(uploaded)
except Exception as e:
    st.error(f"Could not read this file: {e}")
    st.stop()

if raw.empty:
    st.error("The uploaded file has no rows.")
    st.stop()

raw.columns = [str(c).strip() for c in raw.columns]
columns = list(raw.columns)

def guess_col(keywords):
    for c in columns:
        if any(k in c.lower().replace("_", " ") for k in keywords):
            return c
    return "(None)"

st.subheader("1. Match your file columns")
st.caption("Choose which columns represent dates, sales, profit, and optional categories. This lets the dashboard work with different file layouts.")

c1, c2, c3 = st.columns(3)
with c1:
    date_col = st.selectbox("Date column", ["(None)"] + columns,
                            index=(["(None)"] + columns).index(guess_col(["date", "order day", "invoice date"])) if guess_col(["date", "order day", "invoice date"]) in columns else 0)
with c2:
    sales_col = st.selectbox("Sales / Revenue column", ["(None)"] + columns,
                             index=(["(None)"] + columns).index(guess_col(["net sales", "sales", "revenue", "amount", "total"])) if guess_col(["net sales", "sales", "revenue", "amount", "total"]) in columns else 0)
with c3:
    profit_col = st.selectbox("Gross profit column", ["(None)"] + columns,
                              index=(["(None)"] + columns).index(guess_col(["gross profit", "profit", "margin amount"])) if guess_col(["gross profit", "profit", "margin amount"]) in columns else 0)

c4, c5, c6 = st.columns(3)
with c4:
    channel_col = st.selectbox("Channel column (optional)", ["(None)"] + columns,
                               index=(["(None)"] + columns).index(guess_col(["channel", "sales channel", "platform"])) if guess_col(["channel", "sales channel", "platform"]) in columns else 0)
with c5:
    branch_col = st.selectbox("Branch column (optional)", ["(None)"] + columns,
                              index=(["(None)"] + columns).index(guess_col(["branch", "store", "location", "shop"])) if guess_col(["branch", "store", "location", "shop"]) in columns else 0)
with c6:
    discount_col = st.selectbox("Discount column (optional)", ["(None)"] + columns,
                                index=(["(None)"] + columns).index(guess_col(["discount"])) if guess_col(["discount"]) in columns else 0)

if sales_col == "(None)":
    st.warning("Select a sales/revenue column to calculate sales KPIs and charts.")
    st.dataframe(raw.head(10), use_container_width=True)
    st.stop()

df = raw.copy()
df["_sales"] = pd.to_numeric(df[sales_col], errors="coerce").fillna(0)

if profit_col != "(None)":
    df["_profit"] = pd.to_numeric(df[profit_col], errors="coerce")
else:
    df["_profit"] = pd.NA

if discount_col != "(None)":
    df["_discount"] = pd.to_numeric(df[discount_col], errors="coerce").fillna(0)
else:
    df["_discount"] = 0.0

if date_col != "(None)":
    df["_date"] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
else:
    df["_date"] = pd.NaT

if channel_col != "(None)":
    df["_channel"] = df[channel_col].fillna("Unknown").astype(str)
else:
    df["_channel"] = "All records"

if branch_col != "(None)":
    df["_branch"] = df[branch_col].fillna("Unknown").astype(str)
else:
    df["_branch"] = "All records"

st.divider()
st.subheader("2. Filter the dashboard")

f1, f2, f3 = st.columns(3)
filtered = df.copy()

with f1:
    if df["_date"].notna().any():
        min_date = df["_date"].min().date()
        max_date = df["_date"].max().date()
        date_range = st.date_input("Date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
            filtered = filtered[filtered["_date"].between(start, end)]
    else:
        st.caption("No usable date column selected; date filter unavailable.")

with f2:
    channel_options = sorted(filtered["_channel"].dropna().unique().tolist())
    selected_channels = st.multiselect("Channel", channel_options, default=channel_options)
    filtered = filtered[filtered["_channel"].isin(selected_channels)]

with f3:
    branch_options = sorted(filtered["_branch"].dropna().unique().tolist())
    selected_branches = st.multiselect("Branch / Store", branch_options, default=branch_options)
    filtered = filtered[filtered["_branch"].isin(selected_branches)]

if filtered.empty:
    st.warning("No rows match these filters. Change the selected filters.")
    st.stop()

total_sales = filtered["_sales"].sum()
has_profit = filtered["_profit"].notna().any()
total_profit = filtered["_profit"].sum(min_count=1) if has_profit else None
margin = (total_profit / total_sales * 100) if has_profit and total_sales else None
total_discount = filtered["_discount"].sum() if discount_col != "(None)" else None

st.subheader("3. Key performance indicators")
kpis = st.columns(4)
kpis[0].metric("Net sales / Revenue", f"{total_sales:,.2f}")
kpis[1].metric("Gross profit", f"{total_profit:,.2f}" if has_profit else "Not available")
kpis[2].metric("Gross margin", f"{margin:.1f}%" if margin is not None else "Not available")
kpis[3].metric("Discounts", f"{total_discount:,.2f}" if total_discount is not None else "Not available")

st.divider()
st.subheader("4. Interactive charts")

left, right = st.columns(2)

with left:
    st.markdown("**Sales trend over time**")
    if filtered["_date"].notna().any():
        trend = filtered.dropna(subset=["_date"]).copy()
        trend["_period"] = trend["_date"].dt.to_period("M").dt.to_timestamp()
        trend = trend.groupby("_period", as_index=False)["_sales"].sum().sort_values("_period")
        fig = px.line(trend, x="_period", y="_sales", markers=True,
                      labels={"_period": "Month", "_sales": "Sales"},
                      title=None)
        fig.update_traces(line_color=BLUE, line_width=3, marker_size=6)
        fig.update_layout(height=350, margin=dict(l=10, r=10, t=15, b=10),
                          paper_bgcolor="white", plot_bgcolor="white")
        fig.update_yaxes(gridcolor=GRID, zeroline=False)
        fig.update_xaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select a valid date column to display the sales trend.")

with right:
    st.markdown("**Sales by channel**")
    channel_data = filtered.groupby("_channel", as_index=False)["_sales"].sum().sort_values("_sales", ascending=False)
    fig = px.bar(channel_data, x="_channel", y="_sales", text_auto=".2s",
                 labels={"_channel": "Channel", "_sales": "Sales"})
    fig.update_traces(marker_color=BLUE, textposition="outside", cliponaxis=False)
    fig.update_layout(height=350, margin=dict(l=10, r=25, t=15, b=10),
                      paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

left2, right2 = st.columns(2)

with left2:
    st.markdown("**Sales by branch / store**")
    branch_data = filtered.groupby("_branch", as_index=False)["_sales"].sum().sort_values("_sales", ascending=False)
    fig = px.bar(branch_data, x="_sales", y="_branch", orientation="h", text_auto=".2s",
                 labels={"_branch": "Branch / Store", "_sales": "Sales"})
    fig.update_traces(marker_color=GREEN, textposition="outside", cliponaxis=False)
    fig.update_layout(height=350, margin=dict(l=10, r=35, t=15, b=10),
                      paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(showgrid=False, autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

with right2:
    st.markdown("**Sales vs. gross profit**")
    if has_profit:
        valid = filtered.dropna(subset=["_profit"])
        if not valid.empty:
            comparison = pd.DataFrame({
                "Metric": ["Sales", "Gross profit"],
                "Value": [valid["_sales"].sum(), valid["_profit"].sum()]
            })
            fig = px.bar(comparison, x="Metric", y="Value", text_auto=".2s",
                         labels={"Metric": "", "Value": "Amount"})
            fig.update_traces(marker_color=[BLUE, GREEN], textposition="outside", cliponaxis=False)
            fig.update_layout(height=350, margin=dict(l=10, r=25, t=15, b=10),
                              paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
            fig.update_yaxes(gridcolor=GRID, zeroline=False)
            fig.update_xaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("The selected rows have no usable profit values.")
    else:
        st.info("Select a gross profit column above to compare sales and profit.")

if discount_col != "(None)":
    st.markdown("**Discounts by channel**")
    disc = filtered.groupby("_channel", as_index=False)["_discount"].sum().sort_values("_discount", ascending=False)
    fig = px.bar(disc, x="_channel", y="_discount", text_auto=".2s",
                 labels={"_channel": "Channel", "_discount": "Discount"})
    fig.update_traces(marker_color="#F59E0B", textposition="outside", cliponaxis=False)
    fig.update_layout(height=300, margin=dict(l=10, r=25, t=15, b=10),
                      paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("View filtered source rows"):
    st.dataframe(filtered[raw.columns], use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered rows as CSV",
        data=filtered[raw.columns].to_csv(index=False).encode("utf-8-sig"),
        file_name="el_sharnouby_filtered_data.csv",
        mime="text/csv",
    )

st.caption(f"Showing {len(filtered):,} of {len(df):,} rows. Results are calculated from the uploaded file and selected filters.")
