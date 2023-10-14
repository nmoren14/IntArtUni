import sqlite3
import random

# Crear/conectar a la base de datos (esto creará un archivo "transporte.db")
conn = sqlite3.connect('transporte.db')
cursor = conn.cursor()

# Crear una tabla para las rutas (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS rutas (
    id INTEGER PRIMARY KEY,
    medio TEXT,
    inicio TEXT,
    destino TEXT
)
''')

# Limpiar datos anteriores para evitar duplicados
cursor.execute("DELETE FROM rutas")

# Definir datos
medios = ['bus', 'tren', 'metro']
puntos = ['puntoA', 'puntoB', 'puntoC', 'puntoD', 'puntoE']

# Insertar rutas basadas en reglas
# Regla para trenes: conectan puntos consecutivos
for i in range(len(puntos) - 1):
    medio = "tren" + str(i + 1)
    cursor.execute("INSERT INTO rutas (medio, inicio, destino) VALUES (?, ?, ?)", (medio, puntos[i], puntos[i+1]))

# Regla para buses: pueden conectar cualquier punto excepto puntos consecutivos
for _ in range(5):  # Insertar 5 rutas de bus aleatorias
    medio = "bus" + str(random.randint(1, 5))
    inicio = random.choice(puntos)
    destino = random.choice(puntos)
    while abs(puntos.index(inicio) - puntos.index(destino)) == 1 or inicio == destino:
        destino = random.choice(puntos)
    cursor.execute("INSERT INTO rutas (medio, inicio, destino) VALUES (?, ?, ?)", (medio, inicio, destino))

# Regla para metro: conecta el primer y último punto
cursor.execute("INSERT INTO rutas (medio, inicio, destino) VALUES (?, ?, ?)", ("metro1", puntos[0], puntos[-1]))

conn.commit()
conn.close()

print("Base de datos creada con datos basados en reglas.")