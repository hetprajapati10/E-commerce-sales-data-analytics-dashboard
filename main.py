import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit import set_page_config
from streamlit_option_menu import option_menu

set_page_config(page_title='Ecommerce Sales Dashboard',layout="wide")

#======================================================================================================================================
#                                           C   S   S
#======================================================================================================================================
st.markdown("""
<style>

/* ===== IMPORT FUTURISTIC FONT ===== */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

/* ===== MAIN BACKGROUND ===== */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e2e8f0;
    font-family: 'Orbitron', sans-serif;
}

/* ===== GLOBAL FONT ===== */
html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

/* ===== SIDEBAR (GLASS + FIXED) ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(2,6,23,0.95), rgba(15,23,42,0.95));
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Sidebar content */
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ===== FILTERS FIX (NO WHITE BOXES) ===== */
.stMultiSelect, .stSlider, .stSelectbox {
    background-color: transparent !important;
}

/* Dropdown */
div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.05) !important;
    border-radius: 10px;
}

/* Dropdown text */
div[data-baseweb="select"] * {
    color: white !important;
}

/* Slider */
div[data-testid="stSlider"] > div {
    background-color: transparent !important;
}

/* Input fields */
input, textarea {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
}

/* ===== METRIC CARDS (GLASS + HOVER) ===== */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 4px 25px rgba(0,0,0,0.5);
    transition: all 0.3s ease;
}

/* Hover effect */
[data-testid="metric-container"]:hover {
    transform: translateY(-6px);
    box-shadow: 0px 10px 40px rgba(99,102,241,0.4);
}

/* ===== HEADINGS (GAMING STYLE) ===== */
h1 {
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    color: #f8fafc;
    font-weight: 600;
}

/* ===== CHART AREA ===== */
.block-container {
    padding-top: 2rem;
    animation: fadeIn 0.6s ease-in-out;
}

/* Chart card effect */
.element-container {
    background: rgba(255,255,255,0.03);
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
}

/* Remove white chart background */
.js-plotly-plot {
    background-color: transparent !important;
}

/* ===== BUTTONS ===== */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(99,102,241,0.5);
}

/* ===== DATAFRAME ===== */
.stDataFrame {
    background-color: rgba(255,255,255,0.03);
    border-radius: 10px;
}

/* ===== OPTION MENU ===== */
.nav-link {
    font-size: 15px;
    margin-bottom: 5px;
    border-radius: 10px;
    transition: all 0.3s ease;
}

.nav-link:hover {
    background: rgba(99,102,241,0.2);
    transform: translateX(5px);
}

.nav-link-selected {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    box-shadow: 0px 0px 12px rgba(99,102,241,0.6);
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(#6366f1, #8b5cf6);
    border-radius: 10px;
}

/* ===== ANIMATION ===== */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)
#======================================================================================================================================


def load_data():
    df = pd.read_csv("ecommerce.csv")

    # Convert to datetime
    df["listing_date"] = pd.to_datetime(df["listing_date"], errors="coerce")

    # Now this will work
    df["month_year"] = df["listing_date"].dt.to_period("M").astype(str)

    return df
df = load_data()
#------------------sidebar----------------------
with st.sidebar:

#option menu
    selected = option_menu("E-Commerce Sales Analytics Dashboard",
                           ["Home", "Product Analysis", "Pricing & Discounts","Rating & Reviews", "Sales Trend", "Delivery & Logistic","Category Insights"],
                           icons=["house","box","currency-rupee","star","graph-up","truck","pie-chart"])

#filter option in sidebar
    st.subheader("🎛️ Global Filters")

    selected_categories = st.multiselect(
        "Category", options=sorted(df["category"].unique()), default=list(df["category"].unique())
    )
    selected_brands = st.multiselect(
        "Brand", options=sorted(df["brand"].unique()), default=list(df["brand"].unique())
    )
    price_range = st.slider(
        "Final Price Range (₹)",
        int(df["final_price"].min()),
        int(df["final_price"].max()),
        (int(df["final_price"].min()), int(df["final_price"].max())),
    )
    rating_filter = st.slider("Minimum Rating", 1.0, 5.0, 1.0, step=0.1)

    st.markdown("---")
    st.caption("📁 Dataset: Flipkart Products  \n🗂️ 80,000 records · 25 columns")

df["revenue"] = df["final_price"]  # or * units_sold
df["discount_amount"] = df["price"] - df["final_price"]
df["month_year"] = pd.to_datetime(df["month_year"], errors="coerce")

filtered = df[
    (df["category"].isin(selected_categories)) &
    (df["brand"].isin(selected_brands))
]

#Filter Data
filtered = df[
    df["category"].isin(selected_categories)
    & df["brand"].isin(selected_brands)
    & df["final_price"].between(*price_range)
    & (df["rating"] >= rating_filter)
    ]
df["revenue"] = df["final_price"]*df["units_sold"]

COLORS = px.colors.qualitative.Bold

if selected == "Home":
    st.title("E-Commerce Sales Analytics Dashboard")

    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric("📦Total Products",f"{len(filtered):,}")
    col2.metric("Total Revenue",f"{df["revenue"].sum()/1e7:.1f}Cr")
    col3.metric("Avg Rating",f"{filtered["rating"].mean()}")
    col4.metric("Avg Discount", f"{filtered['discount_percent'].mean():.1f}%")
    col5.metric("Units Sold", f"{filtered['units_sold'].sum() / 1e6:.2f}M")

    cat_rev = filtered.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(cat_rev, x="category", y="revenue", color="category",
                 color_discrete_sequence=COLORS,
                 title="💰 Revenue by Category", labels={"revenue": "Revenue (₹)", "category": ""})
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True,key="chart_1")


    cat_count = filtered["category"].value_counts().reset_index()
    cat_count.columns = ["category", "count"]
    fig = px.pie(cat_count, names="category", values="count",
                 title="📦 Product Distribution by Category",
                 color_discrete_sequence=COLORS, hole=0.4)
    fig.update_traces(textposition="outside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True,key="chart_2")


    brand_rev = filtered.groupby("brand")["revenue"].sum().nlargest(10).reset_index()
    fig = px.bar(brand_rev, x="revenue", y="brand", orientation="h",
                 color="revenue", color_continuous_scale="Blues",
                 title="🏆 Top 10 Brands by Revenue")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True,key="chart_3")


    fig = px.box(filtered, x="category", y="rating", color="category",
                 color_discrete_sequence=COLORS,
                 title="⭐ Rating Distribution by Category")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_4")

elif selected == "Product Analysis":
    st.title("📦 Product Analysis")


    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Products", f"{len(filtered):,}")
    col2.metric("Avg Price", f"₹{filtered['final_price'].mean():,.0f}")
    col3.metric("In Stock", f"{filtered['stock_available'].sum():,}")
    col4.metric("Returnable", f"{filtered['is_returnable'].mean()*100:.1f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(filtered, x="final_price", nbins=50, color_discrete_sequence=["#4361ee"],
                           title="💲 Price Distribution", labels={"final_price": "Final Price (₹)"})
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True,key="chart_5")

    with col2:
        fig = px.scatter(filtered.sample(min(2000, len(filtered))), x="final_price", y="units_sold",
                         color="category", color_discrete_sequence=COLORS, opacity=0.6,
                         title="💸 Price vs Units Sold", size_max=10,
                         labels={"final_price": "Price (₹)", "units_sold": "Units Sold"})
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True,key="chart_6")

    col3, col4 = st.columns(2)
    with col3:
        top_units = filtered.groupby("product_name")["units_sold"].sum().nlargest(10).reset_index()
        fig = px.bar(top_units, x="units_sold", y="product_name", orientation="h",
                     color="units_sold", color_continuous_scale="Teal",
                     title="🏅 Top 10 Products by Units Sold")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True,key="chart_7")

    with col4:
        color_sales = filtered.groupby("color")["units_sold"].sum().nlargest(10).reset_index()
        fig = px.bar(color_sales, x="color", y="units_sold", color="color",
                     title="🎨 Top Colors by Units Sold")
        fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True,key="chart_8")

    st.subheader("🔎 Product Explorer")
    search = st.text_input("Search product name")
    show_df = filtered[filtered["product_name"].str.contains(search, case=False, na=False)] if search else filtered
    st.dataframe(
        show_df[["product_name", "category", "brand", "final_price", "rating", "units_sold", "stock_available"]]
        .sort_values("units_sold", ascending=False).head(50),
        use_container_width=True, hide_index=True
    )

#category insights
elif selected == "Category Insights":
    st.title("🏷️ Category Insights")

    cat_summary = filtered.groupby("category").agg(
        Products=("product_id", "count"),
        Revenue=("revenue", "sum"),
        Avg_Price=("final_price", "mean"),
        Avg_Rating=("rating", "mean"),
        Total_Units=("units_sold", "sum"),
        Avg_Discount=("discount_percent", "mean"),
    ).reset_index()


    fig = px.treemap(cat_summary, path=["category"], values="Revenue",
                     color="Avg_Rating", color_continuous_scale="RdYlGn",
                     title="🗺️ Revenue Treemap (colour = avg rating)")
    st.plotly_chart(fig, use_container_width=True)


    fig = px.scatter(cat_summary, x="Avg_Price", y="Avg_Rating", size="Total_Units",
                     color="category", text="category", color_discrete_sequence=COLORS,
                     title="💡 Price vs Rating Bubble Chart")
    fig.update_traces(textposition="top center")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(cat_summary.sort_values("Avg_Discount", ascending=False),
                 x="category", y="Avg_Discount", color="category",
                 color_discrete_sequence=COLORS,
                 title="🏷️ Average Discount % by Category")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


    fig = px.bar(cat_summary.sort_values("Total_Units", ascending=False),
                 x="category", y="Total_Units", color="category",
                 color_discrete_sequence=COLORS,
                 title="📊 Total Units Sold by Category")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Category Summary Table")
    cat_summary["Revenue"] = cat_summary["Revenue"].map("₹{:,.0f}".format)
    cat_summary["Avg_Price"] = cat_summary["Avg_Price"].map("₹{:,.0f}".format)
    cat_summary["Avg_Rating"] = cat_summary["Avg_Rating"].map("{:.2f}".format)
    cat_summary["Avg_Discount"] = cat_summary["Avg_Discount"].map("{:.1f}%".format)
    st.dataframe(cat_summary, use_container_width=True, hide_index=True)

elif selected == "Pricing & Discounts":
    st.title("💰 Pricing & Discounts")


    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg MRP", f"₹{filtered['price'].mean():,.0f}")
    c2.metric("Avg Final Price", f"₹{filtered['final_price'].mean():,.0f}")
    c3.metric("Avg Discount %", f"{filtered['discount_percent'].mean():.1f}%")
    c4.metric("Avg Savings", f"₹{filtered['discount_amount'].mean():,.0f}")


    fig = px.histogram(filtered, x="discount_percent", nbins=40, color="category",
                           color_discrete_sequence=COLORS,
                           title="📉 Discount % Distribution by Category",
                           barmode="overlay", opacity=0.7)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_9")


    disc_cat = filtered.groupby("category")[["price", "final_price"]].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="MRP", x=disc_cat["category"], y=disc_cat["price"],
                         marker_color="#e63946"))
    fig.add_trace(go.Bar(name="Final Price", x=disc_cat["category"], y=disc_cat["final_price"],
                         marker_color="#2a9d8f"))
    fig.update_layout(barmode="group", title="💲 MRP vs Final Price by Category",
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)"
                      , xaxis_title="", yaxis_title="Price (₹)")
    st.plotly_chart(fig, use_container_width=True,key="chart_10")


    fig = px.scatter(filtered.sample(min(3000, len(filtered))), x="discount_percent", y="units_sold",
                     color="category", color_discrete_sequence=COLORS, opacity=0.5,
                     title="📈 Discount % vs Units Sold",
                     labels={"discount_percent": "Discount %", "units_sold": "Units Sold"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


    price_bins = pd.cut(filtered["final_price"], bins=[0, 500, 1000, 3000, 10000, 60000],
                        labels=["<₹500", "₹500-1K", "₹1K-3K", "₹3K-10K", ">₹10K"])
    bin_rev = filtered.groupby(price_bins, observed=True)["revenue"].sum().reset_index()
    fig = px.pie(bin_rev, names="final_price", values="revenue",
                 title="🧩 Revenue Share by Price Band",
                 color_discrete_sequence=COLORS, hole=0.35)
    st.plotly_chart(fig, use_container_width=True,key="chart_11")

    st.subheader("🔥 Highest Discount Products")
    top_disc = filtered.nlargest(10, "discount_percent")[
        ["product_name", "category", "brand", "price", "final_price", "discount_percent", "units_sold"]
    ]
    st.dataframe(top_disc, use_container_width=True, hide_index=True)

#Rating and review
elif selected == "Ratings & Reviews":
    st.title("⭐ Ratings & Reviews")


    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Rating", f"{filtered['rating'].mean():.2f} ⭐")
    c2.metric("Total Reviews", f"{filtered['review_count'].sum():,}")
    c3.metric("5-Star Products", f"{(filtered['rating'] >= 4.5).sum():,}")
    c4.metric("Avg Product Score", f"{filtered['product_score'].mean():.2f}")


    fig = px.histogram(filtered, x="rating", nbins=20, color="category",
                       color_discrete_sequence=COLORS, barmode="overlay", opacity=0.75,
                       title="⭐ Rating Distribution")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_12")


    brand_rating = filtered.groupby("brand").agg(Avg_Rating=("rating", "mean"),
                                                  Products=("product_id", "count")).reset_index()
    fig = px.bar(brand_rating.sort_values("Avg_Rating", ascending=False),
                 x="brand", y="Avg_Rating", color="Avg_Rating",
                 color_continuous_scale="RdYlGn", range_color=[1, 5],
                 title="🏅 Average Rating by Brand")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_13")


    fig = px.scatter(filtered.sample(min(3000, len(filtered))), x="review_count", y="rating",
                     color="category", color_discrete_sequence=COLORS, opacity=0.5,
                     title="📝 Reviews vs Rating",
                     labels={"review_count": "Review Count", "rating": "Rating"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_14")


    fig = px.scatter(filtered.sample(min(3000, len(filtered))), x="rating", y="units_sold",
                     color="category", color_discrete_sequence=COLORS, opacity=0.5,
                     title="📊 Rating vs Units Sold")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_15")

    st.subheader("⭐ Top Rated Products (min 100 reviews)")
    top_rated = filtered[filtered["review_count"] >= 100].nlargest(10, "rating")[
        ["product_name", "category", "brand", "rating", "review_count", "product_score", "units_sold"]
    ]
    st.dataframe(top_rated, use_container_width=True, hide_index=True)

#Sales Trend
elif selected == "Sales Trend":
    st.title("📈 Sales Trends")


    c1, c2, c3 = st.columns(3)
    c1.metric("Date Range", f"{filtered['listing_date'].min().date()} → {filtered['listing_date'].max().date()}")
    c2.metric("Total Revenue", f"₹{filtered['revenue'].sum()/1e7:.2f} Cr")
    c3.metric("Total Units", f"{filtered['units_sold'].sum()/1e6:.2f}M")



    monthly = filtered.groupby("month_year").agg(
        Revenue=("revenue", "sum"),
        Units=("units_sold", "sum"),
        Products=("product_id", "count"),
    ).reset_index().sort_values("month_year")


    fig = px.line(monthly, x="month_year", y="Revenue", markers=True,
                  title="📅 Monthly Revenue Trend", color_discrete_sequence=["#4361ee"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", xaxis_title="Month")
    st.plotly_chart(fig, use_container_width=True,key="chart_16")


    fig = px.line(monthly, x="month_year", y="Units", markers=True,
                  title="📦 Monthly Units Sold", color_discrete_sequence=["#2a9d8f"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", xaxis_title="Month")
    st.plotly_chart(fig, use_container_width=True,key="chart_17")

    cat_monthly = filtered.groupby(["month_year", "category"])["revenue"].sum().reset_index()
    fig = px.line(cat_monthly, x="month_year", y="revenue", color="category",
                  color_discrete_sequence=COLORS, markers=False,
                  title="🗓️ Revenue Trend by Category")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", xaxis_title="Month", yaxis_title="Revenue (₹)")
    st.plotly_chart(fig, use_container_width=True,key="chart_18")


    monthly_new = filtered.groupby("month_year")["product_id"].count().reset_index()
    monthly_new.columns = ["month_year", "new_listings"]
    fig = px.bar(monthly_new, x="month_year", y="new_listings",
                 color="new_listings", color_continuous_scale="Blues",
                 title="🆕 New Product Listings per Month")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_19")


    monthly_rating = filtered.groupby("month_year")["rating"].mean().reset_index()
    fig = px.line(monthly_rating, x="month_year", y="rating", markers=True,
                  title="⭐ Avg Rating Trend Over Time",
                  color_discrete_sequence=["#f4a261"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)", yaxis_range=[1, 5])
    st.plotly_chart(fig, use_container_width=True,key="chart_20")

#delivery and logistic
if selected == "Delivery & Logistic" :
    st.title("🚚 Delivery & Logistics")


    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Delivery Days", f"{filtered['delivery_days'].mean():.1f}")
    c2.metric("Avg Weight (g)", f"{filtered['weight_g'].mean():.0f}")
    c3.metric("Returnable", f"{filtered['is_returnable'].mean() * 100:.1f}%")
    c4.metric("Avg Return Window", f"{filtered['return_policy_days'].mean():.0f} days")


    fig = px.histogram(filtered, x="delivery_days", nbins=20, color="category",
                       color_discrete_sequence=COLORS, barmode="overlay", opacity=0.7,
                       title="🚀 Delivery Days Distribution")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_21")


    del_cat = filtered.groupby("category")["delivery_days"].mean().sort_values().reset_index()
    fig = px.bar(del_cat, x="category", y="delivery_days", color="delivery_days",
                     color_continuous_scale="Oranges",
                     title="📅 Avg Delivery Days by Category")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_22")

    ret_cat = filtered.groupby("category")["is_returnable"].mean().reset_index()
    ret_cat["is_returnable"] *= 100
    fig = px.bar(ret_cat.sort_values("is_returnable", ascending=False),
                 x="category", y="is_returnable", color="is_returnable",
                 color_continuous_scale="Greens",
                 title="↩️ Return Rate % by Category",
                 labels={"is_returnable": "% Returnable"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_23")


    pay_modes = filtered["payment_modes"].str.split(",").explode().str.strip()
    pay_counts = pay_modes.value_counts().reset_index()
    pay_counts.columns = ["mode", "count"]
    fig = px.pie(pay_counts, names="mode", values="count",
                 title="💳 Payment Mode Distribution",
                 color_discrete_sequence=COLORS, hole=0.3)
    st.plotly_chart(fig, use_container_width=True,key="chart_24")

    st.subheader("⚖️ Weight vs Delivery Days")
    fig = px.scatter(filtered.sample(min(2000, len(filtered))), x="shipping_weight_g", y="delivery_days",
                     color="category", color_discrete_sequence=COLORS, opacity=0.5,
                     labels={"shipping_weight_g": "Shipping Weight (g)", "delivery_days": "Delivery Days"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True,key="chart_25")
