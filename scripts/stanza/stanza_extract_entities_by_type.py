import pandas as pd
import stanza

# ---------------- CONFIGURATION ----------------
PATH = "../Inhibidores de proteasa/LOPINAVIR.xlsx"  # Excel file with the reports
NARR_COL = "Narrative and comments"                  # Column with the free-text narratives
DRUG_NAME = "LOPINAVIR"                              # Drug name, used in the output file name
OUTPUT_PATH = f"{DRUG_NAME}_stanza_entities_by_type.xlsx"
# ------------------------------------------------

df = pd.read_excel(PATH)

# Clinical NER pipeline: i2b2 model (PROBLEM, TREATMENT, TEST).
# The model is downloaded only the first time; later runs use the local copy.
stanza.download('en', package='mimic', processors={'ner': 'i2b2'})
nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'i2b2'})


# Analyze the text of one cell and return its entities as (text, type) pairs
def extract(text):
    if pd.isna(text):
        return []  # empty cell: nothing to analyze

    doc = nlp(str(text))
    return [(ent.text.lower().strip(), ent.type) for ent in doc.entities]


df['entities'] = df[NARR_COL].apply(extract)

# Split the entities into columns by type, without duplicates, sorted alphabetically
df['problems'] = df['entities'].apply(lambda items: sorted({term for term, type_ in items if type_ == 'PROBLEM'}))
df['treatments'] = df['entities'].apply(lambda items: sorted({term for term, type_ in items if type_ == 'TREATMENT'}))

# Save the result in a new Excel file
df.to_excel(OUTPUT_PATH, index=False)
print(f"File saved successfully as {OUTPUT_PATH}")
