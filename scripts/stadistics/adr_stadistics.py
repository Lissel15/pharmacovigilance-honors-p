import pandas as pd

PATH = "route_excel.xlsx"                  # Excel file with the reports
ADR_COL = "ADR_col"                        # Column with adverse reactions (comma-separated)
NARR_COL = "narr_col"                      # Column with narratives (used by drug_analysis.py, not here)
DRUG_NAME = "drug_name"                    # Drug name, used in the table and the output file name
OUTPUT_PATH = f"{DRUG_NAME}_reaction_statistics.xlsx"
TOP_N = 50                                 # Number of reactions to report

df = pd.read_excel(PATH)

# Split a cell into a list of unique reactions (they are separated by commas)
def separate(cell):
    if pd.isna(cell):
        return []  # empty cell
    return list({r.strip() for r in str(cell).split(',') if r.strip()})


df['reactions'] = df[ADR_COL].apply(separate)

# Count in how many reports each reaction appears (one count per report)
counts = df['reactions'].explode().value_counts()

# Total number of reports with a reaction recorded
total_reports = df[ADR_COL].notna().sum()

top = counts.head(TOP_N).reset_index()
top.columns = ['Reaction', 'Reports']
top['Percentage'] = (top['Reports'] / total_reports * 100).round(1)
top.insert(0, 'Drug', DRUG_NAME)

print(top)
top.to_excel(OUTPUT_PATH, index=False)
