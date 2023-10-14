import pandas as pd
import random
import sqlite3
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import time

start_time = time.time()

def table_exists(table_name, cursor):
    cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{table_name}' ''')
    return cursor.fetchone()[0] == 1

def setup_database():
    conn = sqlite3.connect('transporte.db')
    cursor = conn.cursor()

    if not table_exists('rutas', cursor):
        cursor.execute('''
        CREATE TABLE rutas (
            id INTEGER PRIMARY KEY,
            medio TEXT,
            inicio TEXT,
            destino TEXT,
            capacidad INTEGER,
            tarifa REAL
        )
        ''')
    else:
        # Intentamos agregar la columna. Si ya existe, SQLite ignorará el comando.
        cursor.execute('ALTER TABLE rutas ADD COLUMN capacidad INTEGER')

    # ... [resto del código de setup_database]
    if not table_exists('horarios', cursor):
        cursor.execute('''
        CREATE TABLE horarios (
            medio TEXT,
            inicio_operacion TEXT,
            fin_operacion TEXT,
            frecuencia INTEGER
        )
        ''')

    if not table_exists('opiniones', cursor):
        cursor.execute('''
        CREATE TABLE opiniones (
            id_ruta INTEGER,
            calificacion INTEGER,
            comentario TEXT
        )
        ''')

    if not table_exists('incidentes', cursor):
        cursor.execute('''
        CREATE TABLE incidentes (
            id_ruta INTEGER,
            descripcion TEXT,
            duracion_retraso INTEGER
        )
        ''')

    if not table_exists('ocupacion_data', cursor):
        cursor.execute('''
        CREATE TABLE ocupacion_data (
            Hora INTEGER,
            Dia INTEGER,
            Ocupacion INTEGER
        )
        ''')
    
    conn.close()

def insert_random_data():
    conn = sqlite3.connect('transporte.db')
    cursor = conn.cursor()

    medios = ['bus', 'tren', 'metro']
    comentarios = ['Buen servicio', 'Demasiado lento', 'Confortable', 'Siempre lleno']

    for medio in medios:
        cursor.execute("INSERT INTO horarios (medio, inicio_operacion, fin_operacion, frecuencia) VALUES (?, ?, ?, ?)",
                       (medio, f"{random.randint(5,7)}:00", f"{random.randint(20,23)}:00", random.randint(5, 20)))

    for i in range(10):
        cursor.execute("INSERT INTO rutas (medio, inicio, destino, capacidad, tarifa) VALUES (?, ?, ?, ?, ?)",
                       (random.choice(medios), f"Punto{chr(65+i)}", f"Punto{chr(66+i)}", random.randint(30, 100), random.uniform(1, 5)))

    for i in range(1, 11):
        cursor.execute("INSERT INTO opiniones (id_ruta, calificacion, comentario) VALUES (?, ?, ?)",
                       (i, random.randint(1, 5), random.choice(comentarios)))

    for i in range(1, 11):
        cursor.execute("INSERT INTO incidentes (id_ruta, descripcion, duracion_retraso) VALUES (?, ?, ?)",
                       (i, random.choice(['Accidente menor', 'Problemas técnicos', 'Mantenimiento']), random.randint(5, 60)))

    conn.commit()
    conn.close()

def insert_occupancy_data(df):
    conn = sqlite3.connect('transporte.db')
    df.to_sql('ocupacion_data', conn, if_exists='replace', index=False)
    conn.close()

def visualize_data(df):
    plt.figure(figsize=(10,6))
    plt.hist(df['Ocupacion'], bins=20, color='blue', alpha=0.7)
    plt.title('Distribución de Ocupación')
    plt.xlabel('Ocupación')
    plt.ylabel('Frecuencia')
    plt.show()

    plt.figure(figsize=(10,6))
    plt.scatter(df['Hora'], df['Ocupacion'], alpha=0.5)
    plt.title('Ocupación por Hora del Día')
    plt.xlabel('Hora')
    plt.ylabel('Ocupación')
    plt.show()

setup_database()
insert_random_data()

data = {
    'Hora': [(i % 24) for i in range(1000)],
    'Dia': [(i % 7) for i in range(1000)],
    'Ocupacion': [random.randint(0, 100) for _ in range(1000)]
}
df = pd.DataFrame(data)
insert_occupancy_data(df)
visualize_data(df)  # Visualizar datos

# Preparar datos para entrenamiento
X = df[['Hora', 'Dia']]
y = df['Ocupacion']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar varios modelos y comparar
models = {
    'DecisionTree': DecisionTreeRegressor(),
    'RandomForest': RandomForestRegressor(),
    'LinearRegression': LinearRegression()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Error Cuadrático Medio para {name}: {mse}")
    
    end_time = time.time()

elapsed_time = end_time - start_time
print(f"El tiempo de ejecución fue: {elapsed_time} segundos")