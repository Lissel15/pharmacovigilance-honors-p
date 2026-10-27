import pandas as pd
#this script needs the excel book creation from vocab_narrative.py
vocab = pd.read_excel('narrative_vocabulary.xlsx')
print('Before:', len(vocab))

# 1. Remove leading articles and possessives: "the rash" -> "rash"
vocab['term'] = (vocab['term'].str.strip()
                 .str.replace(r'^(the|his|her|a|an)\s+', '', regex=True))

# 2. Remove drugs only when they are TREATMENT; PROBLEM terms with a drug name are kept
is_drug = (vocab['type'] == 'TREATMENT') & vocab['term'].str.contains(
    r'avir|vudine|citabine|tenofovir', case=False, na=False)

# 3. Remove generic terms and fragments, of any category.
#    Add or remove terms based on what you see in the data.
NON_VOCAB = {
  #examples:
    'symptoms', 'pregnancy', 'hiv-1 infection', '1 infection', 'treatment',
    'hiv', 'hiv infection', 'antiretroviral therapy', 'iris', 'virological failure'
}
is_non_vocab = vocab['term'].isin(NON_VOCAB)

clean = vocab[~is_drug & ~is_non_vocab]

# 4. Merge duplicates left after removing articles
clean = (clean.groupby(['term', 'type'], as_index=False)['frequency'].sum()
         .sort_values('frequency', ascending=False))

print('After:', len(clean))
print(clean.groupby('type').size())
clean.to_excel('clean_narrative_vocabulary.xlsx', index=False)
