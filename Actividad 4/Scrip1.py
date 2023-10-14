import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Leer los datos desde la base de datos SQLite
conn = sqlite3.connect('transporte.db')
df = pd.read_sql_query("SELECT * FROM ocupacion_data", conn)
conn.close()

# Utilizamos solo las columnas 'Hora' y 'Ocupacion' para el clustering
X = df[['Hora', 'Ocupacion']]

# Asumimos que queremos 3 clusters
kmeans = KMeans(n_clusters=3)
df['cluster'] = kmeans.fit_predict(X)

# Calculamos el promedio de ocupación por hora y por cluster
df_grouped = df.groupby(['Hora', 'cluster']).Ocupacion.mean().reset_index()

# Gráfico de barras
plt.figure(figsize=(12, 7))
sns.barplot(data=df_grouped, x='Hora', y='Ocupacion', hue='cluster', palette='viridis', ci=None)
plt.xlabel('Hora del día')
plt.ylabel('Ocupación promedio')
plt.title('Ocupación promedio por hora del día segmentada por clusters')
plt.legend(title='Cluster')
plt.show()
