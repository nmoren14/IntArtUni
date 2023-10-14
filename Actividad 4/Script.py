import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Leer los datos desde la base de datos SQLite
conn = sqlite3.connect('transporte.db')
df = pd.read_sql_query("SELECT * FROM ocupacion_data", conn)
conn.close()

# Utilizamos solo las columnas 'Hora' y 'Ocupacion' para el clustering
X = df[['Hora', 'Ocupacion']]

# Asumimos que queremos 3 clusters (por ejemplo, baja, media y alta ocupación)
kmeans = KMeans(n_clusters=3)
df['cluster'] = kmeans.fit_predict(X)

# Visualizamos los resultados
plt.scatter(df['Hora'], df['Ocupacion'], c=df['cluster'], cmap='rainbow')
plt.xlabel('Hora')
plt.ylabel('Ocupación')
plt.title('Agrupación de Ocupación por Hora')
plt.show()
