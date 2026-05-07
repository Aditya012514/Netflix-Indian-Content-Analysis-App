import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------

st.set_page_config(
    page_title="Netflix Indian Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM NETFLIX STYLING
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0b0f1a;
}

h1, h2, h3 {
    color: #E50914;
}

.stMetric {
    background-color: #141414;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #E50914;
}

section[data-testid="stSidebar"] {
    background-color: #141414;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

df = pd.read_csv("data/netflix_titles.csv")

# Keep Only Indian Content
df = df[df['country'].fillna('').str.contains('India')]

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.title("🎛 Filter Content")

# Type Filter
selected_type = st.sidebar.selectbox(
    "Select Type",
    ["All"] + list(df['type'].dropna().unique())
)

# Year Filter
selected_year = st.sidebar.slider(
    "Select Release Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    2021
)

# Search Filter
search_movie = st.sidebar.text_input(
    "🔍 Search Title",
    placeholder="Enter movie name..."
)

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered_df = df.copy()

# Filter by Type
if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df['type'] == selected_type
    ]

# Filter by Release Year
filtered_df = filtered_df[
    filtered_df['release_year'] <= selected_year
]

filtered_df = df.copy()
search_df = filtered_df.copy()

# Better Search Filter
if search_movie:

    search_text = search_movie.strip().lower()

    search_df = search_df[
        search_df['title']
        .fillna('')
        .str.lower()
        .str.contains(search_text)
    ]

    # If nothing found
    if filtered_df.empty:

        st.warning(
            "❌ Movie or Web Series not found in dataset"
        )

        st.stop()
# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------

st.title("🎬 Netflix Indian Content Dashboard")

st.markdown("""
## Explore Indian Movies & Web Series with Interactive Analytics
""")

# ---------------------------------------------------
# BANNER IMAGE
# ---------------------------------------------------

st.image(
    "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4",
    use_container_width=True
)

st.write("")

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

total_content = len(filtered_df)

total_movies = len(
    filtered_df[filtered_df['type'] == 'Movie']
)

total_tvshows = len(
    filtered_df[filtered_df['type'] == 'TV Show']
)

latest_year = filtered_df['release_year'].max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎬 Total Content", total_content)
col2.metric("🎥 Movies", total_movies)
col3.metric("📺 TV Shows", total_tvshows)
col4.metric("📅 Latest Release", latest_year)

# ---------------------------------------------------
# FEATURES SECTION
# ---------------------------------------------------

st.subheader("✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 Interactive Dashboard")

with col2:
    st.info("🎥 Indian Movies & Web Series Analysis")

with col3:
    st.info("🤖 Smart Recommendation System")

# ---------------------------------------------------
# ABOUT PROJECT
# ---------------------------------------------------

st.subheader("📌 About This Project")

st.write("""
This project is built using Python, Streamlit, Pandas, and Plotly.

The dashboard helps users:

- Analyze Indian Netflix content
- Explore popular genres
- View release year trends
- Discover movie recommendations
- Interact with visual dashboards
""")

# ---------------------------------------------------
# DATASET PREVIEW
# ---------------------------------------------------

st.subheader("📂 Dataset Preview")

if search_movie:

    if search_df.empty:

        st.warning(
            "❌ Movie or Web Series not found in dataset"
        )

    else:

        st.success(
            f"✅ Found {len(search_df)} result(s)"
        )

        st.dataframe(search_df)

else:

    st.dataframe(filtered_df.head())

# ---------------------------------------------------
# MOVIES VS TV SHOWS
# ---------------------------------------------------

st.subheader("🎭 Overall Movies vs TV Shows Distribution")

type_count = filtered_df['type'].value_counts()

fig = px.bar(
    x=type_count.index,
    y=type_count.values,
    color=type_count.index,
    labels={
        'x': 'Type',
        'y': 'Count'
    },
    title="Overall Indian Netflix Movies vs TV Shows"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# TOP GENRES
# ---------------------------------------------------

st.subheader("🔥 Top Genres")

genre_count = filtered_df['listed_in'].value_counts().head(10)

fig2 = px.bar(
    x=genre_count.values,
    y=genre_count.index,
    orientation='h',
    title="Top Indian Netflix Genres"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# RELEASE YEAR TREND
# ---------------------------------------------------
# ---------------------------------------------------
# RELEASE YEAR TREND
# ---------------------------------------------------

st.subheader("📈 Content Release Trend")

year_data = filtered_df['release_year'].value_counts().sort_index()

# If only one movie/show found
if len(year_data) <= 1:

    st.info(
        "ℹ️ Not enough data to display trend chart"
    )

else:

    fig3 = px.line(
        x=year_data.index,
        y=year_data.values,
        labels={
            'x': 'Year',
            'y': 'Content Count'
        },
        title="Indian Netflix Content Over Years"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# RECOMMENDED SHOWS WITH POSTERS
# ---------------------------------------------------
# RECOMMENDED SHOWS WITH LOCAL POSTERS
# ---------------------------------------------------

st.subheader("🎯 Recommended Indian Shows & Movies")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("assets/Kota Factory.jpg", use_container_width=True)
    st.markdown("### Kota Factory")
    st.write("🎬 Web Series")
    st.write("📅 2021")

with col2:
    st.image("assets/Sacred Games.png", use_container_width=True)
    st.markdown("### Sacred Games")
    st.write("🎬 Crime Thriller")
    st.write("📅 2018")

with col3:
    st.image("assets/Delhi Crime.png", use_container_width=True)
    st.markdown("### Delhi Crime")
    st.write("🎬 Crime Drama")
    st.write("📅 2020")

with col4:
    st.image("assets/Jamtara.png", use_container_width=True)
    st.markdown("### Jamtara")
    st.write("🎬 Thriller")
    st.write("📅 2022")

with col5:
    st.image("assets/Mismatched.png", use_container_width=True)
    st.markdown("### Mismatched")
    st.write("🎬 Romantic Drama")
    st.write("📅 2023")
# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption("Made with ❤️ using Streamlit")