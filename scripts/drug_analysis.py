import pandas as pd
#------------------TOTAL NUMBER OF CASES-----------------------------------------
df = pd.read_excel('route_excel.xlsx', sheet_name='Sheetn')
#cumulative total
cum_total = 0

#number of cases column
num_cases = "num_cases_col"

for valor in df[num_cases]:
    if pd.isna(valor):
        cum_total += 1
    else:
        cum_total += valor

print(f"The total of cases is: {cum_total}")
#-----------------------------------------------------------------------------
#adverse reactions = ar

ar = pd.to_numeric(df['Number of Cases'], errors='coerce').sum()
print(f"Total de casos adversos cuando hubo drug1 en tratamiento: {ar}")


#-----------------------CONDITIONS STADISTICS------------------------------------------------
#palabras clave
cases_w_conditions = {
    "word1": 0,
    "word2": 0,
    "word3": 0,
    "word4": 0,
    "word5": 0,
    "word6": 0

}
#Each row's walkthrough
for indice, fila in df.iterrows():
    full_content = str(fila['narr_col']).lower()
    num_cases = fila['num_cases_col']
    
    # Validation process
    if pd.notna(num_cases) and isinstance(num_cases, (int, float)):
        # at each word
        for condition in cases_w_conditions:
            if condition in full_content:
                # If found, add the value to that specific word in the dictionary
                cases_w_conditions[condition] += num_cases

# final results
for condition, total in cases_w_conditions.items():
    print(f"Total acumulado para '{condition}': {total}")
