import pandas as pd
import numpy as np

df = pd.read_csv(
    "openfoodfacts.csv",
    sep="\t",
    low_memory=False,
    on_bad_lines="skip",
)

# drop emb_codes_tags
df = df.drop(columns=["emb_codes_tags"])

# drop allergens_en due to it having only 1 entries that is also invalid
df = df.drop(columns=["allergens_en"])

# remove identical states and state_tags and rename states_en to states
df = df.drop(columns=["states", "states_tags"])
df = df.rename(columns={"states_en": "states"})


# categories cleaning
# identify invalid values that are often place-holders for missing values
INVALID = {
    "", " ", "?", ".", ",", "n-a", "na", "none", "null", "0",
    "en:null", "en:none"
}

# function that converts junk into missing values before merging
def clean(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip()
    if x.lower() in INVALID:
        return np.nan
    if set(x) <= set("?,.-/ "):   # pure noise
        return np.nan
    return x

cols = ["categories", "categories_tags", "categories_en"]

for c in cols:
    df[c] = df[c].map(clean)

df["categories_final"] = np.nan  # reset 
# create new column through merging
df["categories_final"] = (
    df["categories_en"]
      .fillna(df["categories_tags"])
      .fillna(df["categories"])
)
df = df.drop(columns=["categories", "categories_tags", "categories_en"])

for col in df.columns:
    print("\n" + "="*40)
    print(col)
    
