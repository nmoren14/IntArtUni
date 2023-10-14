import sqlite3

def buscar_rutas(inicio, destino):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('transporte.db')
    cursor = conn.cursor()
    rutas_sugeridas = []
    trasbordos = []

    # Regla para trenes: conectan puntos consecutivos
    if abs(ord(inicio[-1]) - ord(destino[-1])) == 1:
        trenes = cursor.execute("SELECT medio FROM rutas WHERE medio LIKE 'tren%' AND inicio = ? AND destino = ?", (inicio, destino)).fetchall()
        rutas_sugeridas.extend(trenes)

    # Regla para buses: pueden conectar cualquier punto excepto puntos consecutivos
    if abs(ord(inicio[-1]) - ord(destino[-1])) != 1:
        buses = cursor.execute("SELECT medio FROM rutas WHERE medio LIKE 'bus%' AND inicio = ? AND destino = ?", (inicio, destino)).fetchall()
        rutas_sugeridas.extend(buses)

    # Regla para metro: conecta el primer y último punto
    if (inicio == 'puntoA' and destino == 'puntoE') or (inicio == 'puntoE' and destino == 'puntoA'):
        metros = cursor.execute("SELECT medio FROM rutas WHERE medio LIKE 'metro%' AND inicio = ? AND destino = ?", (inicio, destino)).fetchall()
        rutas_sugeridas.extend(metros)

    # Regla de trasbordo: buscar rutas con un cambio de medio de transporte
    puntos_intermedios = cursor.execute("SELECT DISTINCT destino FROM rutas WHERE inicio = ?", (inicio,)).fetchall()
    for punto in puntos_intermedios:
        rutas_intermedias = cursor.execute("SELECT medio FROM rutas WHERE inicio = ? AND destino = ?", (punto[0], destino)).fetchall()
        if rutas_intermedias:
            primero = cursor.execute("SELECT medio FROM rutas WHERE inicio = ? AND destino = ?", (inicio, punto[0])).fetchone()
            trasbordos.append((primero[0], rutas_intermedias[0][0]))

    conn.close()
    return rutas_sugeridas, trasbordos

def main():
    print("Sistema de Consulta de Rutas de Transporte")
    inicio = input("Ingrese el punto de inicio (e.g., puntoA): ")
    destino = input("Ingrese el punto de destino (e.g., puntoB): ")

    rutas, trasbordos = buscar_rutas(inicio, destino)

    if rutas or trasbordos:
        print(f"Rutas sugeridas de {inicio} a {destino}:")
        for ruta in rutas:
            print(f"- Directo: {ruta[0]}")

        for t in trasbordos:
            print(f"- Con trasbordo: {t[0]} -> {t[1]}")
    else:
        print(f"No se encontraron rutas de {inicio} a {destino} según las reglas establecidas.")

if __name__ == "__main__":
    main()
