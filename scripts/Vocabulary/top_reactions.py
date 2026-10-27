import pandas as pd
#this code needs the excel book from vocab_narrative.py

vocab = pd.read_excel('narrative_vocabulary.xlsx')

# Drug name suffixes used to identify drugs (heuristic): -avir, -vudine, -citabine, -tenofovir.
# Adjust this list depending on the main drug under analysis.
is_drug = vocab['term'].str.contains(r'avir|vudine|citabine|tenofovir', case=False, na=False)

# Remove leading articles and possessives: "the rash" -> "rash"
vocab['term'] = vocab['term'].str.replace(r'^(the|his|her|a|an)\s+', '', regex=True)

# Terms that are not adverse reactions
NOT_REACTIONS = {
  #examples:
    'symptoms', 'pregnancy', 'hiv-1 infection', '1 infection',
    'treatment', 'hiv', 'hiv infection', 'antiretroviral therapy',
    'iris', 'virological failure'
}

reactions = vocab[(vocab['type'] == 'PROBLEM') & ~is_drug & ~vocab['term'].isin(NOT_REACTIONS)]

# frequencies, since "rash" and "the rash" are now one term
top = (reactions.groupby('term', as_index=False)['frequency'].sum()
       .sort_values('frequency', ascending=False)
       .head(15))

print(top.to_string(index=False))
top.to_excel('top15_reactions_narratives.xlsx', index=False)
