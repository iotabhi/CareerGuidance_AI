
import pandas as pd
import re

# Load original datasets
df1 = pd.read_csv("data/careerpath_data.csv")
df2 = pd.read_csv("data/roo_data.csv")


# Function to clean text
def clean_text(value):
    if pd.isna(value):
        return ""

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


# Function to extract multiple skills
def extract_items(value):
    if pd.isna(value):
        return []

    items = str(value).split(",")

    return [
        clean_text(item)
        for item in items
        if clean_text(item)
    ]


# Clean Dataset 1
columns1 = [
    "Technical_Skills",
    "Soft_Skills",
    "Fields_of_Interest",
    "Stream",
    "Suggested_Career_Path"
]

for col in columns1:
    df1[col] = df1[col].apply(clean_text)


# Clean Dataset 2
columns2 = [
    "Interested subjects",
    "interested career area ",
    "Suggested Job Role"
]

for col in columns2:
    df2[col] = df2[col].apply(clean_text)


# Extract skills as lists
df1["Technical_Skills_List"] = (
    df1["Technical_Skills"].apply(extract_items)
)

df1["Soft_Skills_List"] = (
    df1["Soft_Skills"].apply(extract_items)
)


# Display cleaned data
print("\n========== CLEANED DATASET 1 ==========")

print(df1[
    ["Technical_Skills", "Technical_Skills_List"]
].head(10).to_string(index=False))


print("\n========== CLEANED DATASET 2 ==========")

print(df2[
    ["Interested subjects", "interested career area "]
].head(10).to_string(index=False))


# Save cleaned datasets
df1.to_csv("data/cleaned_career_path.csv", index=False)
df2.to_csv("data/cleaned_career_roles.csv", index=False)

print("\nPreprocessing completed successfully!")
