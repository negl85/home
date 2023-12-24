import pandas as pd

#a. Extraer la información del archivo. 
# Especifica la ruta del archivo CSV
url_csv = 'https://firebasestorage.googleapis.com/v0/b/tlg-prod.appspot.com/o/assets%2Ffile%2F0.8ddpr74xw650.udno6l076vcountry_vaccinations.csv?alt=media&token=9a0352a1-99c1-41fb-8a61-222c0f9f9e6f'
df=pd.read_csv(url_csv)
print(df.head(8))

print("Info del Dataframe antes de covertir:")
print(df.dtypes)

#b. Mostrar la estructura y tipos de datos de cada columna para identificar qué operaciones puedes realizar con cada una de ellas, asegurándote que las columnas con fechas sean del tipo datetime64. 
#Convertir a datetime64
columnas_fecha = ['date']  # Reemplaza con los nombres reales de tus columnas de fecha
df[columnas_fecha] = df[columnas_fecha].apply(pd.to_datetime, errors='coerce')

# Muestra la estructura y tipos de datos de cada columna después de la conversión
print("\nInformación del DataFrame después de la conversión:")
print(df.dtypes)

#c. Determinar la cantidad de vacunas aplicadas de cada compañía (con base en cómo lo reporta cada país en la columna vaccines, en otras palabras, agrupe por vaccines y realice la sumatoria). 
vacunas_por_marca = df.groupby('vaccines')['total_vaccinations'].sum()

print("Cantidad de vacunas por marca:")
print(vacunas_por_marca)

#d. Obtener la cantidad de vacunas aplicadas en todo el mundo. 
columna_a_sumar = 'total_vaccinations'
suma_total = df[columna_a_sumar].sum()
# Resultado
print(f"La suma total de la columna '{columna_a_sumar}' es: {suma_total}")

#e. Calcular el promedio de vacunas aplicadas por país. 
vacunas_por_pais = df.groupby('country')['total_vaccinations'].mean()
print("Promedio de vacunas por país:")
print(vacunas_por_pais)

#f. Determinar la cantidad de vacunas aplicadas el día 29/01/21 en todo el mundo.
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df_29_enero = df[df['date'].dt.date == pd.to_datetime('2021-01-29').date()]

total_vacunas_29_enero = df_29_enero['total_vaccinations'].sum()

print("Vacunas aplicadas el 29/01/21 en todo el mundo:")
print(total_vacunas_29_enero)

#g. Crear un dataframe nuevo denominado conDiferencias que contenga los datos originales y una columna derivada (diferencias) con las diferencias de aplicación entre las columnas daily_vaccionations y daily_vaccionations_raw. 
#Nuevo dataframe
conDiferencias = df.copy()
conDiferencias['diferencias'] = df['daily_vaccinations']-df['daily_vaccinations_raw']
print(conDiferencias)

#h. Obtener el periodo de tiempo entre el registro con fecha más reciente y el registro con fecha más antigua. 
fecha_mas_reciente = df['date'].max()
fecha_mas_antigua = df['date'].min()
periodo_tiempo = fecha_mas_reciente - fecha_mas_antigua
print(f"Fecha más reciente: {fecha_mas_reciente}")
print(f"Fecha más antigua: {fecha_mas_antigua}")
print(f"Período de tiempo entre registros: {periodo_tiempo}")

#i. Crear un dataframe nuevo denominado conCantidad que contenga los datos originales y una columna derivada (canVac) con la cantidad de vacunas utilizadas cada día (usar la columna vaccines y separar por el carácter , ). 
#Nuevo dataframe
conCantidad = df.copy()
vacunas_separadas = df['vaccines'].str.split(',', expand=True)
conCantidad['canVac'] = vacunas_separadas.apply(pd.to_numeric, errors='coerce').sum(axis=1)
print(conCantidad)

#j. Generar un dataframe denominado antes20 con todos los registros que se hayan realizado antes del 20 de diciembre de 2020. 

antes20=df[df['date']<'2020-12-20']
print("Registros antes del 20 de diciembre:")
print(antes20)

#k. Obtener un dataframe denominado pfizer con todos los registros donde se haya utilizado la vacuna Pfizer. 
pfizer = df[df['vaccines'].str.contains('Pfizer', case=False, na=False)]
print("Vacuna Pfizer:")
print(pfizer)

#l. Almacenar los dataframes generados (conDiferencias, conCantidad, antes20 y pfizer) en un archivo de Excel denominado resultadosReto.xlsx, donde cada dataframe ocupe una hoja diferente. 
# Almacenar los DataFrames en un archivo Excel


# Crear el nuevo DataFrame conDiferencias
nombre_archivo = r'C:\Users\NGAMEZ\Desktop\resultadosReto4.xlsx'
with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
    try:
        # Almacena cada DataFrame en una hoja diferente
        conDiferencias.to_excel(writer, sheet_name='conDiferencias', index=False)
        conCantidad.to_excel(writer, sheet_name='conCantidad', index=False)
        antes20.to_excel(writer, sheet_name='antes20', index=False)
        pfizer.to_excel(writer, sheet_name='pfizer', index=False)

        print(f"Se ha creado el archivo '{nombre_archivo}' con las hojas correspondientes.")
    except Exception as e:
        print(f"Error al escribir en el archivo de Excel: {e}")