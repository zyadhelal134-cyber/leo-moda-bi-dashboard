import pandas as pd
import plotly.express as px
import streamlit as st

# ==================================================
# 1. PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="LEO MODA | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# 2. DESIGN SYSTEM & HEADER FIXES
# ==================================================
BG = "#0B1120"
PANEL = "#111A2B"
BORDER = "#253249"
BLUE = "#60A5FA"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* إخفاء الهيدر الافتراضي لمنع أي تداخل نصوص في أعلى الصفحة */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 1;
}

.stApp {
    background: #0B1120;
    color: #F1F5F9;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0F172A;
    border-right: 1px solid #253249;
}

[data-testid="stSidebar"] h1 {
    font-size: 23px;
    font-weight: 800;
    color: #F8FAFC;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #CBD5E1;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1600px;
}

h1, h2, h3 {
    color: #F1F5F9 !important;
    letter-spacing: -0.5px;
}

[data-testid="stMetric"] {
    background: #111A2B;
    border: 1px solid #253249;
    padding: 20px 18px;
    border-radius: 14px;
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 13px;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-size: 27px;
    font-weight: 700;
}

div[data-testid="stPlotlyChart"] {
    background: #111A2B;
    border: 1px solid #253249;
    border-radius: 14px;
    padding: 10px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #253249;
    border-radius: 12px;
}

.section-caption {
    color: #94A3B8;
    font-size: 13px;
    margin-top: -6px;
    margin-bottom: 22px;
}

.brand-tag {
    color: #60A5FA;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.insight-box {
    background-color: #1E293B;
    border-left: 4px solid #60A5FA;
    padding: 16px;
    border-radius: 8px;
    color: #E2E8F0;
    font-size: 14px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. LOAD CLEANED & AUXILIARY DATA
# ==================================================
@st.cache_data
def load_data():
    files = {
        "sales": "cleaned_data/Sales_Transactions_Cleaned.csv",
        "inventory": "cleaned_data/Inventory_History_Cleaned.csv",
        "production": "cleaned_data/Production_Orders_Cleaned.csv",
        "marketing": "cleaned_data/Marketing_Cleaned.csv",
        "purchase": "cleaned_data/Purchase_Orders_Cleaned.csv",
        "service": "cleaned_data/Customer_Service_Cleaned.csv",
        "traffic": "cleaned_data/Web_Traffic_Daily_Cleaned.csv",
        "downtime": "Machine_Downtime.csv",
        "materials": "Materials.csv",
    }

    loaded = {}
    for key, path in files.items():
        try:
            loaded[key] = pd.read_csv(path)
        except Exception:
            alt_path = path.replace("cleaned_data/", "")
            loaded[key] = pd.read_csv(alt_path)

    return loaded


try:
    data = load_data()
    sales_df = data["sales"]
    inv_df = data["inventory"]
    prod_df = data["production"]
    mkt_df = data["marketing"]
    po_df = data["purchase"]
    cs_df = data["service"]
    web_df = data["traffic"]
    dt_df = data["downtime"]
    mat_df = data["materials"]

except Exception as e:
    st.error("Unable to load data files. Please ensure all CSV files exist in the project directory.")
    st.exception(e)
    st.stop()


# ==================================================
# 4. REUSABLE FUNCTIONS
# ==================================================
def money(value):
    return f"{value:,.0f} EGP"


def style_chart(fig, horizontal=False):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color=TEXT,
            size=12,
        ),
        margin=dict(l=15, r=20, t=35, b=15),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor=PANEL,
            font_color=TEXT,
        ),
    )

    fig.update_xaxes(
        showgrid=not horizontal,
        gridcolor=BORDER,
        zeroline=False,
        linecolor=BORDER,
    )
    fig.update_yaxes(
        showgrid=horizontal,
        gridcolor=BORDER,
        zeroline=False,
        linecolor=BORDER,
    )

    return fig


def section_header(title, subtitle):
    st.markdown(
        f'<div class="brand-tag">LEO MODA / ANALYTICS</div>',
        unsafe_allow_html=True,
    )
    st.title(title)
    st.markdown(
        f'<div class="section-caption">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def show_chart(fig, horizontal=False):
    fig = style_chart(fig, horizontal=horizontal)
    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# 5. SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown("## LEO MODA")
    st.caption("EL-SHARNOUBY GROUP")
    st.divider()

    st.markdown("**BUSINESS OVERVIEW**")

    pages = [
        "Executive Overview",
        "Inventory & Replenishment",
        "Customer Intelligence",
        "Factory & Production",
        "Marketing Performance",
        "Branch Intelligence & Expansion",
        "Procurement & Suppliers",
        "Size & Fit Intelligence",
    ]

    app_choice = st.radio(
        "Navigate",
        pages,
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("BUSINESS INTELLIGENCE (Cleaned Data)")
    st.caption("Data period: Oct 2023 – Sep 2026")
    st.caption("Currency: Egyptian Pound (EGP)")


# ==================================================
# 6. EXECUTIVE OVERVIEW
# ==================================================
if app_choice == "Executive Overview":
    section_header(
        "Executive Overview",
        "A clear view of sales, profitability and business performance.",
    )

    metric_row([
        ("Gross Sales", money(sales_df["Gross_Sales_EGP"].sum())),
        ("Net Sales", money(sales_df["Net_Sales_EGP"].sum())),
        ("Gross Profit", money(sales_df["Gross_Profit_EGP"].sum())),
        ("Units Sold", f'{sales_df["Quantity"].sum():,.0f}'),
        (
            "Avg. Gross Margin",
            f'{sales_df["Gross_Margin_Pct"].mean() * 100:.1f}%'
        ),
    ])

    st.divider()

    left, right = st.columns([1.35, 1])

    with left:
        st.subheader("Revenue & Profit by Channel")

        summary = (
            sales_df.groupby("Channel", as_index=False)
            .agg(
                Net_Sales=("Net_Sales_EGP", "sum"),
                Gross_Profit=("Gross_Profit_EGP", "sum"),
            )
        )

        fig = px.bar(
            summary,
            x="Channel",
            y=["Net_Sales", "Gross_Profit"],
            barmode="group",
            color_discrete_sequence=[BLUE, "#34D399"],
            labels={
                "value": "Amount (EGP)",
                "variable": "Metric",
                "Channel": "Sales Channel",
            },
        )
        show_chart(fig)

    with right:
        st.subheader("Top Locations by Revenue")

        locations = (
            sales_df.groupby("Location_Name", as_index=False)
            ["Net_Sales_EGP"].sum()
            .sort_values("Net_Sales_EGP", ascending=True)
            .tail(10)
        )

        fig = px.bar(
            locations,
            x="Net_Sales_EGP",
            y="Location_Name",
            orientation="h",
            color_discrete_sequence=[BLUE],
            labels={
                "Net_Sales_EGP": "Net Sales (EGP)",
                "Location_Name": "Location",
            },
        )
        show_chart(fig, horizontal=True)

    st.divider()
    st.subheader("Sales Transactions")
    st.dataframe(
        sales_df.head(100),
        use_container_width=True,
        hide_index=True,
    )


# ==================================================
# 7. INVENTORY & REPLENISHMENT
# ==================================================
elif app_choice == "Inventory & Replenishment":
    section_header(
        "Inventory & Replenishment",
        "Monitor stock availability and identify replenishment priorities.",
    )

    metric_row([
        ("Inventory Records", f"{len(inv_df):,}"),
        (
            "Products Tracked",
            f'{inv_df["Product_ID"].nunique():,}'
            if "Product_ID" in inv_df.columns else "N/A"
        ),
        (
            "Locations Tracked",
            f'{inv_df["Location_Name"].nunique():,}'
            if "Location_Name" in inv_df.columns else "N/A"
        ),
    ])

    st.divider()

    if "Product_ID" in inv_df.columns:
        st.subheader("Inventory History")
        st.dataframe(
            inv_df,
            use_container_width=True,
            hide_index=True,
        )


# ==================================================
# 8. CUSTOMER INTELLIGENCE
# ==================================================
elif app_choice == "Customer Intelligence":
    section_header(
        "Customer Intelligence",
        "Understand customer value and identify your highest-spending customers.",
    )

    metric_row([
        ("Unique Customers", f'{sales_df["Customer_ID"].nunique():,}'),
        ("Average Order Value", money(sales_df["Net_Sales_EGP"].mean())),
        (
            "Total Transactions",
            f'{sales_df["Invoice_ID"].nunique():,}'
        ),
    ])

    st.divider()
    st.subheader("Top 10 Customers by Spending")

    customer_summary = (
        sales_df.groupby("Customer_ID", as_index=False)
        .agg(
            Total_Spent=("Net_Sales_EGP", "sum"),
            Total_Orders=("Invoice_ID", "nunique"),
        )
        .sort_values("Total_Spent", ascending=False)
        .head(10)
    )

    st.dataframe(
        customer_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total_Spent": st.column_config.NumberColumn(
                "Total Spending (EGP)", format="%,.2f"
            ),
            "Total_Orders": st.column_config.NumberColumn(
                "Unique Orders", format="%d"
            ),
        },
    )

    fig = px.bar(
        customer_summary.sort_values("Total_Spent"),
        x="Total_Spent",
        y="Customer_ID",
        orientation="h",
        color_discrete_sequence=[BLUE],
        labels={
            "Total_Spent": "Total Spending (EGP)",
            "Customer_ID": "Customer",
        },
    )
    show_chart(fig, horizontal=True)


# ==================================================
# 9. FACTORY & PRODUCTION
# ==================================================
elif app_choice == "Factory & Production":
    section_header(
        "Factory & Production",
        "Track production efficiency, quality, overtime and machine downtime.",
    )

    total_downtime = dt_df["Downtime_Hours"].sum() if "Downtime_Hours" in dt_df.columns else 0

    metric_row([
        ("Avg. Efficiency", f'{prod_df["Efficiency_Pct"].mean():.1f}%'),
        ("Rejected Units", f'{prod_df["Rejected_Qty"].sum():,.0f}'),
        ("Overtime Hours", f'{prod_df["Overtime_Hours"].sum():,.1f}'),
        ("Total Machine Downtime", f'{total_downtime:,.1f} Hrs'),
    ])

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("Efficiency by Production Line")
        efficiency = (
            prod_df.groupby("Line_ID", as_index=False)
            ["Efficiency_Pct"].mean()
        )

        fig = px.bar(
            efficiency,
            x="Line_ID",
            y="Efficiency_Pct",
            color_discrete_sequence=[BLUE],
            labels={
                "Line_ID": "Production Line",
                "Efficiency_Pct": "Efficiency (%)",
            },
        )
        show_chart(fig)

    with right:
        st.subheader("Rejected Units by Line")
        rejected = (
            prod_df.groupby("Line_ID", as_index=False)
            ["Rejected_Qty"].sum()
        )

        fig = px.pie(
            rejected,
            names="Line_ID",
            values="Rejected_Qty",
            hole=0.6,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        show_chart(fig)

    # --- Machine Downtime Analysis ---
    st.divider()
    st.subheader("Machine Downtime Analysis")

    dt_left, dt_right = st.columns([1.3, 1])

    with dt_left:
        reason_summary = (
            dt_df.groupby("Reason", as_index=False)
            ["Downtime_Hours"].sum()
            .sort_values("Downtime_Hours", ascending=True)
        )
        fig_dt = px.bar(
            reason_summary,
            x="Downtime_Hours",
            y="Reason",
            orientation="h",
            color_discrete_sequence=["#F87171"],
            labels={
                "Downtime_Hours": "Downtime (Hours)",
                "Reason": "Downtime Reason",
            },
        )
        show_chart(fig_dt, horizontal=True)

    with dt_right:
        planned_summary = (
            dt_df.groupby("Planned", as_index=False)
            ["Downtime_Hours"].sum()
        )
        fig_planned = px.pie(
            planned_summary,
            names="Planned",
            values="Downtime_Hours",
            hole=0.5,
            color_discrete_sequence=["#EF4444", "#10B981"],
        )
        show_chart(fig_planned)

    st.subheader("Production Orders Table")
    st.dataframe(prod_df, use_container_width=True, hide_index=True)


# ==================================================
# 10. MARKETING PERFORMANCE
# ==================================================
elif app_choice == "Marketing Performance":
    section_header(
        "Marketing Performance",
        "Compare campaign spending, attributed revenue and return on ad spend.",
    )

    marketing = mkt_df.copy()
    marketing["ROAS"] = (
        marketing["Attributed_Revenue_EGP"]
        / marketing["Spend_EGP"].replace(0, float("nan"))
    )

    total_spend = marketing["Spend_EGP"].sum()
    total_revenue = marketing["Attributed_Revenue_EGP"].sum()
    overall_roas = total_revenue / total_spend if total_spend else 0

    metric_row([
        ("Total Ad Spend", money(total_spend)),
        ("Attributed Revenue", money(total_revenue)),
        ("Blended ROAS", f"{overall_roas:.2f}x"),
    ])

    st.divider()
    st.subheader("Spend vs Attributed Revenue")

    platform = (
        marketing.groupby("Platform", as_index=False)
        .agg(
            Spend=("Spend_EGP", "sum"),
            Revenue=("Attributed_Revenue_EGP", "sum"),
        )
    )

    fig = px.bar(
        platform,
        x="Platform",
        y=["Spend", "Revenue"],
        barmode="group",
        color_discrete_sequence=["#A78BFA", "#34D399"],
        labels={
            "value": "Amount (EGP)",
            "variable": "Metric",
        },
    )
    show_chart(fig)


# ==================================================
# 11. BRANCH INTELLIGENCE & EXPANSION
# ==================================================
elif app_choice == "Branch Intelligence & Expansion":
    section_header(
        "Branch Intelligence & Store Expansion",
        "Compare location-level performance and analyze regional demand for new store expansion.",
    )

    branches = (
        sales_df.groupby("Location_Name", as_index=False)
        .agg(
            Net_Sales=("Net_Sales_EGP", "sum"),
            Gross_Profit=("Gross_Profit_EGP", "sum"),
            Avg_Gross_Margin=("Gross_Margin_Pct", "mean"),
        )
        .sort_values("Net_Sales", ascending=False)
    )

    metric_row([
        ("Active Locations", f'{branches["Location_Name"].nunique():,}'),
        ("Total Net Sales", money(branches["Net_Sales"].sum())),
        ("Total Gross Profit", money(branches["Gross_Profit"].sum())),
    ])

    st.divider()

    st.markdown("### 📍 Where to open the next store")
    st.markdown("**Greater Cairo buys online as much as Alexandria — with no store**")

    online_sales = sales_df[sales_df["Channel"] == "Online"].copy()

    gov_summary = (
        online_sales.groupby("Customer_Governorate", as_index=False)
        .agg(
            Online_Sales_EGP=("Net_Sales_EGP", "sum"),
            Online_Customers=("Customer_ID", "nunique"),
        )
    )

    cairo_giza = gov_summary[gov_summary["Customer_Governorate"].isin(["Cairo", "Giza"])]
    cairo_sales = cairo_giza["Online_Sales_EGP"].sum()
    cairo_cust = cairo_giza["Online_Customers"].sum()

    other_govs = gov_summary[~gov_summary["Customer_Governorate"].isin(["Cairo", "Giza"])].copy()

    greater_cairo_df = pd.DataFrame([{
        "Customer_Governorate": "Greater Cairo",
        "Online_Sales_EGP": cairo_sales,
        "Online_Customers": cairo_cust
    }])

    expansion_df = pd.concat([greater_cairo_df, other_govs], ignore_index=True)
    expansion_df["Online_Sales_M"] = expansion_df["Online_Sales_EGP"] / 1e6
    expansion_df = expansion_df.sort_values("Online_Sales_M", ascending=False)

    expansion_df["Has_Store"] = expansion_df["Customer_Governorate"].apply(
        lambda x: "Yes (Sidi Bishr)" if x == "Alexandria" else "No"
    )

    left_chart, right_table = st.columns([1.3, 1])

    with left_chart:
        color_map = {
            "Greater Cairo": "#F97316",
            "Alexandria": "#3B82F6",
        }
        expansion_df["Color"] = expansion_df["Customer_Governorate"].map(lambda x: color_map.get(x, "#64748B"))

        fig = px.bar(
            expansion_df.sort_values("Online_Sales_M", ascending=True),
            x="Online_Sales_M",
            y="Customer_Governorate",
            orientation="h",
            color="Color",
            color_discrete_map="identity",
            text_auto=".1f",
            labels={
                "Online_Sales_M": "Online Sales (3 Years EGP Millions)",
                "Customer_Governorate": "Region",
            },
        )
        fig.update_traces(texttemplate="%{x:.1f}M", textposition="outside")
        show_chart(fig, horizontal=True)

    with right_table:
        st.dataframe(
            expansion_df[["Customer_Governorate", "Online_Sales_M", "Online_Customers", "Has_Store"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Customer_Governorate": "Region",
                "Online_Sales_M": st.column_config.NumberColumn("Online Sales (M)", format="%.1fM"),
                "Online_Customers": st.column_config.NumberColumn("Online Customers", format="%d"),
                "Has_Store": "Store?",
            }
        )

        st.markdown("""
        <div class="insight-box">
            💡 <b>Greater Cairo (Cairo + Giza)</b> generates the same online sales volume as Alexandria (~9.3M EGP), despite having no physical store.<br><br>
            <b>Recommended Next Step:</b> Launch a pop-up store or shop-in-shop in Cairo for 3 months to capture physical retail demand and measure conversion vs online baseline.
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# 12. PROCUREMENT & SUPPLIERS
# ==================================================
elif app_choice == "Procurement & Suppliers":
    section_header(
        "Procurement & Suppliers",
        "Monitor purchase orders, supplier delivery delay and quality issues.",
    )

    po = po_df.copy()
    if "Promised_Date" in po.columns and "Actual_Receipt_Date" in po.columns:
        po["Promised_Date"] = pd.to_datetime(po["Promised_Date"])
        po["Actual_Receipt_Date"] = pd.to_datetime(po["Actual_Receipt_Date"])
        po["Delay_Days"] = (po["Actual_Receipt_Date"] - po["Promised_Date"]).dt.days
        avg_delay = po["Delay_Days"].mean()
    else:
        avg_delay = 0

    metric_row([
        ("Purchase Orders", f"{len(po):,}"),
        ("Rejected Quantity", f'{po["Rejected_Qty"].sum():,.0f}'),
        ("Suppliers Tracked", f'{po["Supplier_ID"].nunique():,}' if "Supplier_ID" in po.columns else "N/A"),
        ("Avg Delivery Delay", f"{avg_delay:.1f} Days"),
    ])

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rejected Quantities by Supplier")
        supplier_summary = (
            po.groupby("Supplier_ID", as_index=False)
            ["Rejected_Qty"].sum()
            .sort_values("Rejected_Qty", ascending=False)
        )

        fig = px.bar(
            supplier_summary,
            x="Supplier_ID",
            y="Rejected_Qty",
            color="Rejected_Qty",
            color_continuous_scale="Reds",
            labels={
                "Supplier_ID": "Supplier",
                "Rejected_Qty": "Rejected Quantity",
            },
        )
        show_chart(fig)

    with col2:
        st.subheader("Average Supplier Lead Time Delay (Days)")
        delay_summary = (
            po.groupby("Supplier_ID", as_index=False)
            ["Delay_Days"].mean()
            .sort_values("Delay_Days", ascending=False)
        )

        fig_delay = px.bar(
            delay_summary,
            x="Supplier_ID",
            y="Delay_Days",
            color="Delay_Days",
            color_continuous_scale="Oranges",
            labels={
                "Supplier_ID": "Supplier",
                "Delay_Days": "Avg Delay (Days)",
            },
        )
        show_chart(fig_delay)

    st.subheader("Purchase Orders Table")
    st.dataframe(po, use_container_width=True, hide_index=True)


# ==================================================
# 13. SIZE & FIT INTELLIGENCE
# ==================================================
elif app_choice == "Size & Fit Intelligence":
    section_header(
        "Size & Fit Intelligence",
        "Explore customer service data to identify opportunities to reduce fit-related returns.",
    )

    metric_row([
        ("Service Records", f"{len(cs_df):,}"),
        ("Traffic Records", f"{len(web_df):,}"),
        (
            "Customer IDs Available",
            "Yes" if "Customer_ID" in cs_df.columns else "Not identified"
        ),
    ])

    st.divider()
    st.subheader("Customer Service Data")
    st.dataframe(
        cs_df.head(200),
        use_container_width=True,
        hide_index=True,
    )


# ==================================================
# 14. FOOTER
# ==================================================
st.divider()
st.caption(
    "LEO MODA | El-Sharnouby Group · Business Intelligence Dashboard (Cleaned Data)"
)