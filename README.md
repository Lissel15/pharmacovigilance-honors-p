# Pharmacovigilance Research🔬: adverse drug reaction statistics for protease inhibitors
## By ⚙️Lissel Erandi Flores Polvo.⚙️

Scripts for descriptive statistics and vocabulary extraction from pharmacovigilance reports on protease inhibitors (honors thesis project). They work on Excel databases, one drug at a timeime.

> Status: work in progress. Some scripts still need the paths and column names set for your data.

## Repository structure💻

```
.
├── README.md
├── research_journal/
└── scripts/
    ├── adr_stadistics.py            # reaction counts per report
    ├── drug_analysis.py             # keyword analysis per drug (template)
    └── vocabulario/
        ├── vocab_reactions.py       # vocabulary from the structured reactions column
        ├── vocab_narrative.py       # vocabulary from narratives (Stanza, i2b2 NER)
        ├── clean_narrative_vocab.py # cleans the narrative vocabulary
        └── top_reactions.py
       # top 15 reactions from the narrative vocabulary 
```

## Configuration 

Every script has a configuration block at the top. Set these variables before running a script:

| Variable | Meaning | Example |
|---|---|---|
| `PATH` | Excel file with the reports | `"route_excel.xlsx"` |
| `ADR_COL` | Column with adverse reactions, separated by commas | `"ADR_col"` |
| `NARR_COL` | Column with the free-text narratives | `"narr_col"` |
| `DRUG_NAME` | Name of the drug, used in tables and output file names | `"drug_name"` |
| `NUM_CASES` | Column with number of cases | `"num_cases_col"` |

Only change these values. Do not change the rest of the code unless you are modifying the analysis.

## Requirements

- Python 3.9 or later
- pandas and openpyxl (to read and write `.xlsx` files)
- stanza (only for the narrative vocabulary scripts)
- requests (only for `buscar_cui.py`)

```bash
pip install pandas openpyxl stanza requests
```

## Expected data format

- **ADR_COL:** reactions separated by commas, for example `Weight gain drug-induced, Insulin resistance drug-induced`.
- **NARR_COL:** free-text narrative for each report.
- **Number of Cases:** used by `drug_analysis.py`. Empty cells are counted as 1.

## Usage

### Reaction statistics

```bash
python scripts/adr_stadistics.py
```

Output: `<DRUG_NAME>_reaction_statistics.xlsx`, with the columns `Drug`, `Reaction`, `Reports` and `Percentage`. Each report counts once per reaction, even if the reaction is repeated in the same cell.

### Narrative vocabulary

Run the scripts in this order, from the `scripts/vocabulario/` folder:

```bash  
python vocab_reactions.py         # reaction vocabulary from ADR_COL
python vocab_narrative.py         # narrative vocabulary (Stanza)
python clean_narrative_vocab.py   # cleaned vocabulary
python top_reacciones.py          # top 15 reactions
```
### Keyword analysis (templates)

`drug_analysis.py` is a template. Replace the placeholder keywords and file names before running it.

## Notes📓

- Keyword searches match substrings. "rash" also matches "rashes" or "the rash".
- Counts per report (`adr_stadistics.py`) are different from mention counts in free text. Do not describe mention counts as reports.
- Drug suffixes used to identify drugs (`avir`, `vudine`, `citabine`, `tenofovir`) are a heuristic. Adjust them for each main drug.

## Data📊

The original data is not included in this repository. If data is added, it must not contain information that identifies patients.
