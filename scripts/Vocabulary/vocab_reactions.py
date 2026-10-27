import pandas as pd

# Change this path to your Excel route
RUTA = "route_excel.xlsx"
COL = "ADR_col"

df = pd.read_excel(RUTA)

# 1. Split each cell by commas, strip spaces, and lowercase
terms = (
    df[COL].dropna()
    .astype(str)
    .str.split(',')
    .explode()
    .str.strip()
    .str.lower()
)
terms = terms.str.replace(r'\s*drug[- ]induced\s*$', '', regex=True).str.strip()

# 2. Vocabulary: unique terms with their frequency
  vocab = terms.value_counts().rename_axis('Term').reset_index(name='Frecuency')

print(f"Unique terms: {len(vocab)}")
print(f"Total mentions: {len(terminos)}")
print(vocab.head(15))

  vocab.to_excel('vocabulary_reactions.xlsx', index=False)
