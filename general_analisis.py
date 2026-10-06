import pandas as pd
from pathlib import Path

# Lista de tus archivos de Excel
books = [ 
    'CARPETA_ORIGEN/LIBRO1.xlsx',
    'CARPETA_ORIGEN/LIBRO2.xlsx',
    'CARPETA_ORIGEN/LIBRO3.xlsx',
    'CARPETA_ORIGEN/LIBRO4.xlsx',
    'CARPETA_ORIGEN/LIBRO5.xlsx',
    'CARPETA_ORIGEN/LIBRO6.xlsx'
]

palabras_clave = ["palabra1", "palabra 2", "palabra n"]
tabla_resultados = []

for rute in books:
    # Cargar el archivo
    df = pd.read_excel(rute, sheet_name='Sheet0')
    
    # Calcular el total de casos (ajustando nulos a 1 como en tu lógica)
    ar = 0
    # En CELDA se colcoa el nombre de la celda que tenga los valores numéricos
    for valor in df['CELDA']:
        valor_num = pd.to_numeric(valor, errors='coerce')
        if pd.isna(valor_num):
            ar += 1
        else:
            ar += valor_num
            
    # Inicializar conteos para este archivo
    conteo_condiciones = {palabra: 0 for palabra in palabras_clave}
    
    for indice, fila in df.iterrows():
        #En NARRATIVE AND COMMENTS se coloca la celda con contenido en lenguaje natural
        full_content = str(fila['Narrative and comments']).lower()
        #Se vuelve a referencias la celda con datos numéricos
        num_cases = fila['CELDA']
        
        if pd.notna(num_cases) and isinstance(num_cases, (int, float)):
            for condition in conteo_condiciones:
                if condition in full_content:
                    conteo_condiciones[condition] += num_cases
                    
    # Calcular porcentajes y guardarlos en un diccionario temporal
    fila_datos = {"Medicamento": Path(rute).stem}
    for condition, total in conteo_condiciones.items():
        porcentaje = (total / ar * 100) if ar > 0 else 0
        fila_datos[condition] = round(porcentaje, 2)
        
    tabla_resultados.append(fila_datos)

# Crear el DataFrame final con pandas
df_final = pd.DataFrame(tabla_resultados)
df_final.set_index("Medicamento", inplace=True)

print(df_final)




# variables: patologias, antecedentes 