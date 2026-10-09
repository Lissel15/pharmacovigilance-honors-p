import pandas as pd
#acceso a bases de datos en excel
#personalizar las siguientes variables
# --CARPETA (carpeta de origen)
# --EXCEL (nombre del excel como base de datos)
# --ADR (nombre de la columna con las reacciones adversas)
# --nombre_excel.xlsx (nombre del nuevo excel que contendrá las estadísticas)

df = pd.read_excel('CARPETA/EXCEL.xlsx')

#columna con reacciones adversas
columna = 'ADR'

#función para separa reacciones adversas, pues vienen separadas por una coma

def separate(celda):
    if pd.isna(celda):
        return [] #checa si la celda está vacía
    return list({r.strip() for r in str(celda).split(',') if r.strip()})
    #se separa por comas y se limpia el texto

df['reacciones']=df[columna].apply(separate)

#se hace el conteo de en cuantos reportes aparece la reacción, se cuenta por fila
conteo=df['reacciones'].explode().value_counts()

#se toma el total de reportes
total_reportes = df [columna].notna().sum()
top=conteo.head(50).reset_index()
top.columns=['Reacción', 'Reportes']
top['Porcentaje']= (top['Reportes']/total_reportes*100).round(1)

print(top)
top.to_excel('nombre_excel.xlsx', index=False)
