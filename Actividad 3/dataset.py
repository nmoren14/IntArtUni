import pandas as pd
import random

# Generar datos aleatorios para el dataset
data = {
    'Hora': [(i % 24) for i in range(1000)],  # Hora del día (0-23)
    'Dia': [(i % 7) for i in range(1000)],    # Día de la semana (0-6)
    'Ocupacion': [random.randint(0, 100) for _ in range(1000)]  # Porcentaje de ocupación (0-100)
}

df = pd.DataFrame(data)