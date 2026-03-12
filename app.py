import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide"
)

# -------------------------------------------------
# HEADER (LOGO + TITLE)
# -------------------------------------------------

col1, col2 = st.columns([1,6])

with col1:
    st.image("Google-Play-Logo.png", width=120)

with col2:
    st.title("Google Play Store Analytics Dashboard")
   

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_apps.csv")
    return df

df = load_data()

# -------------------------------------------------
# TOP METRICS
# -------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Apps", len(df))
col2.metric("Total Categories", df["Category"].nunique())
col3.metric("Total Reviews", int(df["Reviews"].sum()))
col4.metric("Average Rating", round(df["Rating"].mean(), 2))

st.markdown("---")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["EDA Analysis", "Clustering Insights", "Recommendation System"]
)

# =================================================
# 1️⃣ EDA SECTION
# =================================================
if page == "EDA Analysis":
    st.title("📊 Exploratory Data Analysis")

    # --- Free vs Paid Apps ---
    st.subheader("Free vs Paid Apps Distribution")
    type_count = df["Type"].value_counts()
    fig = px.pie(
        names=type_count.index,
        values=type_count.values,
        hole=0.4,
        title="Free vs Paid Apps"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Top 5 Categories ---
    st.subheader("Top 5 App Categories")
    top_categories = df['Category'].value_counts().reset_index()
    top_categories.columns = ['Category', 'Count']
    fig = px.bar(
        top_categories.head(5),
        x='Category',
        y='Count',
        text='Count',
        color='Count',
        color_continuous_scale='Blues',
        title="Top 5 App Categories"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # --- Installs by Category ---
    st.subheader("Installs by Category")
    installs_category = df.groupby("Category")["Installs"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(
        installs_category.head(10),
        x="Category",
        y="Installs",
        color="Installs",
        title="Top Categories by Installs"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # --- Reviews vs Average Rating by Category ---
    st.subheader("Reviews vs Average Rating by Category")
    rating_reviews = df.groupby("Category").agg({"Rating":"mean","Reviews":"sum"}).reset_index()
    
    # Line chart for Avg Rating
    fig = px.line(
        rating_reviews.sort_values('Rating', ascending=False),
        x='Category',
        y='Rating',
        title='Average Rating by Category'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart for Reviews
    fig = px.bar(
        rating_reviews.sort_values('Reviews', ascending=False),
        x='Category',
        y='Reviews',
        title='Total Reviews by Category',
        color='Reviews',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Rating Distribution ---
    st.subheader("Rating Distribution")
    fig = px.histogram(df, x="Rating", nbins=30, title="Distribution of App Ratings")
    st.plotly_chart(fig, use_container_width=True)

# =================================================
# 2️⃣ CLUSTER SECTION
# =================================================
elif page == "Clustering Insights":
    st.title("🧠 App Clustering Analysis")
    st.markdown("Clustering performed on Rating, Reviews, Installs, and Price (K-Means).")

    if "Cluster" in df.columns:
        st.subheader("App Clusters (Installs vs Rating)")
        fig = px.scatter(
            df,
            x="Installs",
            y="Rating",
            color="Cluster",
            log_x=True,
            hover_data=["App"],
            title="App Clusters"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Cluster Summary Table")
        cluster_summary = df.groupby('Cluster')[['Rating','Reviews','Installs','Price']].mean().round(2)
        st.dataframe(cluster_summary)

        st.subheader("Cluster Interpretation (Hidden Patterns)")
        st.markdown("""
**Cluster 0 – Paid Moderate**
- Apps with moderate installs, mostly paid
- Niche/specialized apps

**Cluster 1 – Popular Free**
- High installs, many reviews
- Mostly free apps dominating the Play Store

**Cluster 2 – Top Free**
- Extremely high installs
- Massive user engagement
- Examples: Social Media / Communication apps

📊 **Insight:** Free apps dominate, paid apps are niche with moderate installs.
""")
    else:
        st.warning("Cluster column not found in dataset.")

# =================================================
# 3️⃣ RECOMMENDATION SYSTEM
# =================================================
elif page == "Recommendation System":
    st.title("🤖 App Recommendation System")
    st.markdown("Filter apps by category, type, and minimum rating.")

    col1, col2, col3 = st.columns(3)
    category = col1.selectbox("Category", sorted(df["Category"].unique()))
    app_type = col2.selectbox("Type", df["Type"].dropna().unique())
    min_rating = col3.slider("Minimum Rating", 1.0, 5.0, 4.0)

    if st.button("Recommend Apps"):
        results = df[
            (df["Category"] == category) &
            (df["Type"] == app_type) &
            (df["Rating"] >= min_rating)
        ].sort_values(by=["Rating","Reviews"], ascending=False)

        if len(results) > 0:
            st.success(f"{len(results)} apps found")
            st.dataframe(results[['App','Category','Rating','Reviews','Installs','Price']].head(10))
        else:
            st.warning("No apps found with these filters.")