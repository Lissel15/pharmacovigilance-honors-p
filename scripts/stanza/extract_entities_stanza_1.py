import pandas as pd
import stanza

# ---------------- CONFIGURATION ----------------
PATH = "ADISINSIGHT 2/ATAZANAVIR.xlsx"    # Excel file with the reports
NARR_COL = "Narrative and comments"        # Column with the free-text narratives
DRUG_NAME = "ATAZANAVIR"                   # Drug name, used in the output file name
OUTPUT_PATH = f"{DRUG_NAME}_extracted_entities.xlsx"
# ------------------------------------------------

df = pd.read_excel(PATH)

# Clinical NER pipeline: i2b2 model (PROBLEM, TREATMENT, TEST).
# The model is downloaded only the first time; later runs use the local copy.
stanza.download('en', package='mimic', processors={'ner': 'i2b2'})
nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'i2b2'})


# Analyze the text of one cell and return its entities as "text (type)"
def extract_entities(text):
    if pd.isna(text):
        return []  # empty cell: nothing to analyze

    doc = nlp(str(text))
    return [f"{ent.text} ({ent.type})" for ent in doc.entities]


# Apply the function to the narrative column
df['extracted_entities'] = df[NARR_COL].apply(extract_entities)

# Save the result in a new Excel file
df.to_excel(OUTPUT_PATH, index=False)
print(f"File saved successfully as {OUTPUT_PATH}")
