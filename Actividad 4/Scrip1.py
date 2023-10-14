import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear un directorio para guardar las visualizaciones
if not os.path.exists('results'):
    os.makedirs('results')

# 1. Prueba de Conexión a la Base de Datos
try:
    conn = sqlite3.connect('transporte.db')
    print("Conexión a la base de datos establecida con éxito.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# 2. Prueba de Lectura de Datos
try:
    df = pd.read_sql_query("SELECT * FROM ocupacion_data", conn)
    print(f"Datos leídos correctamente. {df.shape[0]} registros cargados.")
except Exception as e:
    print(f"Error al leer datos: {e}")
finally:
    conn.close()

# 3. Prueba de Clustering con KMeans
try:
    X = df[['Hora', 'Ocupacion']]
    kmeans = KMeans(n_clusters=3)
    df['cluster'] = kmeans.fit_predict(X)
    print("Clustering realizado exitosamente.")
except Exception as e:
    print(f"Error durante el clustering: {e}")

# 4. Prueba de Cálculo de Promedios
try:
    df_grouped = df.groupby(['Hora', 'cluster']).Ocupacion.mean().reset_index()
    print("Cálculo de promedios realizado exitosamente.")
except Exception as e:
    print(f"Error al calcular promedios: {e}")

# 5. Prueba de Visualización
try:
    plt.figure(figsize=(12, 7))
    sns.barplot(data=df_grouped, x='Hora', y='Ocupacion', hue='cluster', palette='viridis', ci=None)
    plt.xlabel('Hora del día')
    plt.ylabel('Ocupación promedio')
    plt.title('Ocupación promedio por hora del día segmentada por clusters')
    plt.legend(title='Cluster')
    plt.savefig('results/ocupacion_promedio_clusters.png')  # Guardamos la visualización en un archivo
    print("Visualización generada y guardada en 'results/ocupacion_promedio_clusters.png'.")
    plt.show()
except Exception as e:
    print(f"Error en la visualización: {e}")
