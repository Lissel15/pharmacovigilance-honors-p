# Pharmacovigilance Research 🔬: adverse drug reaction statistics for protease inhibitors

Descriptive statistics scripts for pharmacovigilance reports on protease inhibitors (honors thesis project). They compute adverse reaction frequencies and case counts by condition from Excel databases.

> Status: templates. The scripts contain placeholders (`CARPETA`, `ADR`, `word1`, `CELDA`, etc.) that must be replaced before running. They do not include patient data.

## Contents

| File | What it does |
|---|---|
| `scripts/adr_stadistics.py` | Counts the number of reports in which each adverse reaction appears and computes its percentage over the total number of reports. |
| `scripts/drug_analysis.py` | For one drug: adjusted total of cases and case counts per keyword in the narratives. |
| `scripts/general_analisis.py` | Same as `drug_analysis.py`, but for several files at once, with a comparison table of percentages. |

## Requirements

- Python 3.9 or later
- pandas
- openpyxl (to read and write `.xlsx` files)

```bash
pip install pandas openpyxl
```

## Expected data format

The databases are Excel files with at least these columns:

- **Adverse Events** (or the name you set in `ADR`): adverse reactions separated by commas.
- **Number of Cases**: number of cases per report. Empty cells are counted as 1 in `drug_analysis.py`.
- **Narrative and comments**: free-text narrative, used to search for keywords.

## Usage

### 1. 💊`adr_stadistics.py`

1. Replace `CARPETA` and `EXCEL` in the `pd.read_excel` path.
2. Change `columna = 'ADR'` to the actual name of the reactions column.
3. Change `nombre_excel.xlsx` to the output file name.
4. Run:

```bash
python scripts/adr_stadistics.py
```

Output: a table of the 50 most frequent reactions, with columns `Reacción`, `Reportes` and `Porcentaje`. Each report counts once per reaction, even if the reaction appears more than once in the same cell.

### 2. 💊`drug_analysis.py`

1. Replace `CARPETA_ORIGEN/DRUG1.xlsx` with the database for the drug.
2. Define the keywords in `cases_w_conditions` (`word1`, `word2`, ...).
3. Run:

```bash
python scripts/drug_analysis.py
```

Output: adjusted total of cases, total adverse cases, and accumulated cases for each keyword.

### 3. 💊`general_analisis.py`

1. Replace the `books` list with the paths to the databases.
2. Define the keywords in `palabras_clave`.
3. Replace `CELDA` with the name of the numeric column (usually `Number of Cases`), and `Narrative and comments` if it has a different name.
4. Run:

```bash
python scripts/general_analisis.py
```

Output: a table with one row per drug and the percentage of cases that mention each keyword.

## 📓Notes

- `drug_analysis.py` and `general_analisis.py` match keywords as substrings. "rash" also matches "rashes" or "the rash".
- Some scripts use `isinstance(valor, (int, float))` to validate numbers. Pandas can return `numpy.int64`, which fails that check; `pd.to_numeric` is safer.
- Reaction counts in `adr_stadistics.py` are per report. Mention counts from free text are not reports.

## 📊Data

The original data is not included in this repository. If data is added, it must not contain information that identifies patients.
