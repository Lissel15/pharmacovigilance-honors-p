import re
import pandas as pd

# ---------------- CONFIGURATION ----------------
PATH = "Inhibidores de proteasa/ATAZANAVIR.xlsx"  # Excel file with the reports
SHEET_NAME = 0                                    # Sheet to read: 0 = first sheet, or a name such as "Sheet0"
ADR_COL = "Adverse Events"                        # Column with adverse reactions (not used in this script)
NARR_COL = "Narrative and comments"               # Column with the free-text narratives
NUM_CASES = "Number of Cases"                     # Column with the number of cases per report
DRUG_NAME = "ATAZANAVIR"                          # Drug name, used in the output file name
KEYWORDS = ["hiv", "pregnant", "covid-19", "copd", "woman", "man"]  # Examples, you should keep them in lowercase
OUTPUT_PATH = f"{DRUG_NAME}_keyword_statistics.xlsx"
# ------------------------------------------------

df = pd.read_excel(PATH, sheet_name=SHEET_NAME)

# Adjusted total: empty cells count as 1 case
adjusted_total = 0
for value in df[NUM_CASES]:
    if pd.isna(value):
        adjusted_total += 1
    else:
        adjusted_total += value

# Reported total: empty cells are ignored
reported_cases = pd.to_numeric(df[NUM_CASES], errors='coerce').sum()

print(f"Adjusted total cases for {DRUG_NAME}: {adjusted_total}")
print(f"Reported cases for {DRUG_NAME}: {reported_cases}")

# Cases per keyword: each report adds its cases to every keyword found in its narrative.
# Whole-word matching (\b) avoids false matches, for example "man" inside "woman".
keyword_cases = {keyword: 0 for keyword in KEYWORDS}
for _, row in df.iterrows():
    narrative = str(row[NARR_COL]).lower()
    cases = pd.to_numeric(row[NUM_CASES], errors='coerce')
    if pd.notna(cases):
        for keyword in KEYWORDS:
            if re.search(rf"\b{re.escape(keyword)}\b", narrative):
                keyword_cases[keyword] += cases

results = pd.DataFrame({
    'Drug': DRUG_NAME,
    'Keyword': list(keyword_cases.keys()),
    'Cases': list(keyword_cases.values()),
})
if reported_cases > 0:
    results['Percentage'] = (results['Cases'] / reported_cases * 100).round(2)
else:
    results['Percentage'] = 0

print(results.to_string(index=False))
results.to_excel(OUTPUT_PATH, index=False)
