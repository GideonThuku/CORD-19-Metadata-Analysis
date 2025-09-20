
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud   # pip install wordcloud
import numpy as np

pd.set_option('display.max_columns', 40)

DATA_PATH = "metadata.csv"  

def load_data(path=DATA_PATH, nrows=None):
    print("Loading data:", path)
    df = pd.read_csv(path, nrows=nrows)
    print("Loaded shape:", df.shape)
    return df

def basic_explore(df):
    print("\n--- Head ---")
    print(df.head(3).T)
    print("\n--- Info ---")
    print(df.info())
    print("\n--- Missing values (top columns) ---")
    print(df.isnull().sum().sort_values(ascending=False).head(20))

def clean_data(df):
    df = df.copy()
    # Standardize publish date column name variations:
    if 'publish_time' not in df.columns and 'publish_year' in df.columns:
        df['publish_time'] = df['publish_year'].astype(str)
    # Parse dates
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    # Extract year (int)
    df['year'] = df['publish_time'].dt.year
    # Fill missing journals
    if 'journal' in df.columns:
        df['journal'] = df['journal'].fillna("Unknown")
    # Create abstract word count
    if 'abstract' in df.columns:
        df['abstract_word_count'] = df['abstract'].fillna("").str.split().str.len()
    else:
        df['abstract_word_count'] = np.nan
    # Keep important columns
    return df

def analysis_plots(df, outdir="plots"):
    os.makedirs(outdir, exist_ok=True)

    # Publications by year
    year_counts = df['year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(x=year_counts.index.astype(int).astype(str), y=year_counts.values, ax=ax)
    ax.set_title("Publications by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(os.path.join(outdir, "publications_by_year.png"))
    print("Saved:", os.path.join(outdir, "publications_by_year.png"))
    plt.close(fig)

    # Top journals
    if 'journal' in df.columns:
        top_j = df['journal'].value_counts().head(15)
        fig, ax = plt.subplots(figsize=(8,6))
        sns.barplot(y=top_j.index, x=top_j.values, ax=ax)
        ax.set_title("Top 15 Journals (by paper count)")
        ax.set_xlabel("Count")
        ax.set_ylabel("Journal")
        plt.tight_layout()
        fig.savefig(os.path.join(outdir, "top_journals.png"))
        print("Saved:", os.path.join(outdir, "top_journals.png"))
        plt.close(fig)

    # Distribution of abstract word count
    if 'abstract_word_count' in df.columns:
        fig, ax = plt.subplots(figsize=(6,4))
        sns.histplot(df['abstract_word_count'].dropna(), bins=50, kde=False, ax=ax)
        ax.set_title("Abstract word count distribution")
        ax.set_xlabel("Words")
        plt.tight_layout()
        fig.savefig(os.path.join(outdir, "abstract_wordcount.png"))
        print("Saved:", os.path.join(outdir, "abstract_wordcount.png"))
        plt.close(fig)

    # Word cloud of titles (optional)
    if 'title' in df.columns:
        titles = df['title'].dropna().astype(str).str.cat(sep=' ')
        wc = WordCloud(width=800, height=400, background_color="white", max_words=150).generate(titles)
        fig, ax = plt.subplots(figsize=(10,5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        fig.savefig(os.path.join(outdir, "title_wordcloud.png"))
        print("Saved:", os.path.join(outdir, "title_wordcloud.png"))
        plt.close(fig)

def top_journals_table(df, n=10):
    if 'journal' in df.columns:
        return df['journal'].value_counts().head(n)
    return pd.Series(dtype=int)

def main():
    # If dataset is huge, you can set nrows=200000 or None for full file
    df = load_data(nrows=None)
    basic_explore(df)
    df = clean_data(df)
    print("\nYear counts (example):")
    print(df['year'].value_counts().sort_index().tail(10))
    print("\nTop journals:")
    print(top_journals_table(df, 10))

    analysis_plots(df)

    # Save cleaned sample for app use
    sample = df.sample(n=min(2000, len(df)), random_state=1)
    sample.to_csv("metadata_clean_sample.csv", index=False)
    print("Saved sample for app: metadata_clean_sample.csv (rows=%d)" % len(sample))

if __name__ == "__main__":
    main()
