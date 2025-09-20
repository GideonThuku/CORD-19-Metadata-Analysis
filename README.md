# CORD-19 Metadata Analysis

This project looks at the **CORD-19 Dataset** (a collection of COVID-19 research papers) and tries to find useful information such as:
- Number of papers published over time  
- Top research areas and keywords  
- Most active authors and institutions  

The goal is to make it easier to understand how COVID-19 research grew and what topics were most studied.

---

## Project Files

- **app.py** – Main script that runs the analysis  
- **analysis.py** – Helper functions for data cleaning and processing  
- **metadata.csv** – The main dataset (large file, stored using Git LFS)  
- **requirements.txt** – List of Python libraries needed  
- **README.md** – This file  

---

## Setup Instructions

###
Follow these steps to set up and run the project on your computer.

### 1. Clone the Repository
``bash
git clone https://github.com/GideonThuku/CORD-19-Metadata-Analysis.git
cd CORD-19-Metadata-Analysis

### 2. Install Python Libraries

Make sure you have Python installed.
Then install all required packages:

pip install -r requirements.txt

### 3. Set Up Git LFS (Large Files)

This project uses Git LFS
 because the dataset is large.
Run these commands if you haven’t already:

git lfs install
git lfs pull

Running the Analysis

To run the analysis:

python app.py


You can also open analysis.py if you want to look at or edit how the data is processed.

### Example Output

The script will generate:

Basic statistics about the dataset

A list of top authors

Publication trends over time
