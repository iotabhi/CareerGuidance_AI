
import pandas as pd
df1 = pd.read_csv("data/careerpath_data.csv")
df2 = pd.read_csv("data/roo_data.csv")

# Display dataset information
print("\n========== DATASET 1 ==========")
print("Shape:", df1.shape)
print("\nColumns:")
print(df1.columns.tolist())
print("\nFirst 5 rows:")
print(df1.head())
print("\nMissing values:")
print(df1.isnull().sum())

print("\n========== DATASET 2 ==========")
print("Shape:", df2.shape)
print("\nColumns:")
print(df2.columns.tolist())
print("\nFirst 5 rows:")
print(df2.head())
print("\nMissing values:")
print(df2.isnull().sum())

# =====================================
# STEP 8: DEEP DATASET EXPLORATION
# =====================================

print("\n========== DATASET 1 EXPLORATION ==========")

# Career categories
print("\nCareer distribution:")
print(df1["Suggested_Career_Path"].value_counts())

# Data types
print("\nData types:")
print(df1.dtypes)

# Duplicate records
print("\nDuplicate records:", df1.duplicated().sum())

# Sample technical skills
print("\nTechnical skills examples:")
print(df1["Technical_Skills"].head(10).to_list())

# Sample interests
print("\nInterest examples:")
print(df1["Fields_of_Interest"].head(10).to_list())


print("\n========== DATASET 2 EXPLORATION ==========")

# Career categories
print("\nJob role distribution:")
print(df2["Suggested Job Role"].value_counts())

# Data types
print("\nData types:")
print(df2.dtypes)

# Duplicate records
print("\nDuplicate records:", df2.duplicated().sum())

# Sample interested subjects
print("\nInterested subjects:")
print(df2["Interested subjects"].head(10).to_list())

# Sample career areas
print("\nInterested career areas:")
print(df2["interested career area "].head(10).to_list())

import matplotlib.pyplot as plt

# Career distribution - Dataset 1
career_counts1 = df1["Suggested_Career_Path"].value_counts()

plt.figure(figsize=(12, 7))
career_counts1.plot(kind="bar")
plt.title("Career Distribution - Dataset 1")
plt.xlabel("Career")
plt.ylabel("Number of Students")
plt.xticks(rotation=75, ha="right")
plt.tight_layout()
plt.savefig("assets/career_distribution_1.png")
plt.show()


# Career distribution - Dataset 2
career_counts2 = df2["Suggested Job Role"].value_counts()

plt.figure(figsize=(13, 7))
career_counts2.plot(kind="bar")
plt.title("Job Role Distribution - Dataset 2")
plt.xlabel("Job Role")
plt.ylabel("Number of Students")
plt.xticks(rotation=80, ha="right")
plt.tight_layout()
plt.savefig("assets/career_distribution_2.png")
plt.show()

# STEP 10: Inspect important categorical values

print("\n========== DATASET 1 ==========")

columns1 = [
    "Technical_Skills",
    "Soft_Skills",
    "Fields_of_Interest",
    "Stream",
    "Suggested_Career_Path"
]

for col in columns1:
    print(f"\n{col}:")
    print(df1[col].value_counts().head(15))


print("\n========== DATASET 2 ==========")

columns2 = [
    "Interested subjects",
    "interested career area ",
    "Suggested Job Role"
]

for col in columns2:
    print(f"\n{col}:")
    print(df2[col].value_counts().head(15))
