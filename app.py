# app.py - Streamlit CORD-19 Data Explorer
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CORD-19 Explorer", layout="wide")

@st.cache_data
def load_sample(path="metadata_clean_sample.csv"):
    return pd.read_csv(path)

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of CORD-19 metadata (sample)")

# Load data with caching
try:
    df = load_sample()
except FileNotFoundError:
    st.error("metadata_clean_sample.csv not found. Run analysis.py first to create a sample file.")
    st.stop()

# Sidebar controls
st.sidebar.header("Filters")
years = sorted([int(x) for x in df['year'].dropna().unique() if not pd.isna(x)])
if len(years) == 0:
    st.sidebar.write("No year info available")
    year_min, year_max = None, None
else:
    year_min = int(min(years))
    year_max = int(max(years))
    sel_years = st.sidebar.slider("Select year range", year_min, year_max, (max(year_min, year_max-2), year_max))

# Apply year filter
if year_min is not None:
    filtered = df[(df['year'] >= sel_years[0]) & (df['year'] <= sel_years[1])]
else:
    filtered = df.copy()

st.markdown(f"### Showing {len(filtered)} papers (years {sel_years[0]}–{sel_years[1]})")

# Publications by year plot
st.subheader("Publications by year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8,3))
sns.barplot(x=year_counts.index.astype(int).astype(str), y=year_counts.values, ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Count")
plt.xticks(rotation=45)
st.pyplot(fig)

# Top journals
st.subheader("Top journals")
if 'journal' in filtered.columns:
    top_j = filtered['journal'].value_counts().head(10)
    st.bar_chart(top_j)

# Show sample table and allow download
st.subheader("Data sample")
st.dataframe(filtered.head(50))

csv = filtered.to_csv(index=False)
st.download_button("Download filtered data as CSV", csv, file_name="cord19_filtered.csv", mime="text/csv")
