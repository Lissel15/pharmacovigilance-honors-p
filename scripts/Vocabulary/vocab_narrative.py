import pandas as pd
import stanza

# Change this path to your Excel file
ROUTE = "route_excel.xlsx"
COL = "narr_col"
MAIN_DRUG = "drug_name"

df = pd.read_excel(ROUTE)

# Clinical NER pipeline: i2b2 model (PROBLEM, TREATMENT, TEST)
nlp = stanza.Pipeline("en", package="mimic", processors={"ner": "i2b2"})


# Extract entities from each narrative, excluding the main drug
def extract(text):
    if pd.isna(text):
        return []
    doc = nlp(str(text))
    return [(ent.text.lower().strip(), ent.type)
            for ent in doc.entities
            if ent.text.lower().strip() != MAIN_DRUG]


df["entities"] = df[COL].apply(extract)

# Unique terms per category with their frequency
rows = [(t, tipo) for lista in df["entities"] for t, tipo in lista]
vocab = (pd.DataFrame(rows, columns=["term", "type"])
           .value_counts()
           .reset_index(name="frequency")
           .sort_values("frequency", ascending=False))

# Remaining variants of the main drug name, to review
variants = vocab[vocab["term"].str.contains(MAIN_DRUG, case=False, na=False)]
print(variants)
print(f"Unique terms: {len(vocab)}")
print(vocab.groupby("type").size())
vocab.to_excel("narrative_vocabulary.xlsx", index=False)

# Presence matrix per report, using the 50 most frequent terms
top = vocab.head(50)["term"].unique()
for t in top:
    df[f"has_{t}"] = df["entities"].apply(lambda l: int(any(x == t for x, _ in l)))

df.drop(columns=["entities"]).to_excel("narrative_matrix.xlsx", index=False)
