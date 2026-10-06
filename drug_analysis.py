
#ritonavir
import pandas as pd
#------------------NÚMERO DE CASOS TOTALES-----------------------------------------
df = pd.read_excel('CARPETA_ORIGEN/DRUG1.xlsx', sheet_name='Sheet0')
total_acumulado = 0
#columna de número de casos
num_cases = "Number of Cases"

for valor in df[num_cases]:
    
    # Si la celda está vacía o no es un número válido (NaN), sumamos 1
    if pd.isna(valor):
        total_acumulado += 1
    else:
        # Si sí es un número, sumamos su valor real
        total_acumulado += valor

print(f"El total ajustado es: {total_acumulado}")
#-----------------------------------------------------------------------------
#adverse reactions = ar
# reaccciones adversas en total en todos los casos registrados
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
#recorrido de cada fila
for indice, fila in df.iterrows():
    full_content = str(fila['Narrative and comments']).lower()
    num_cases = fila['Number of Cases']
    
    # Validamos que el número sea válido
    if pd.notna(num_cases) and isinstance(num_cases, (int, float)):
        # Revisamos cada palabra de nuestro diccionario
        for condition in cases_w_conditions:
            if condition in full_content:
                # Si la encuentra, suma el valor a esa palabra específica en el diccionario
                cases_w_conditions[condition] += num_cases

# Mostramos los resultados finales
for condition, total in cases_w_conditions.items():
    print(f"Total acumulado para '{condition}': {total}")

