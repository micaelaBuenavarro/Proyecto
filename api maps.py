import sqlite3
import googlemaps  # type: ignore

API_KEY = 'AIzaSyDuXWNWR3lIiQWgJBEoYR_ldhr-VSk6470'

def crear_base():
    conn = sqlite3.connect("ubicaciones.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ubicaciones (
            usuario TEXT PRIMARY KEY,
            direccion TEXT,
            lat REAL,
            lon REAL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_ubicacion(usuario, direccion, lat, lon):
    conn = sqlite3.connect("ubicaciones.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO ubicaciones (usuario, direccion, lat, lon)
        VALUES (?, ?, ?, ?)
    ''', (usuario, direccion, lat, lon))
    conn.commit()
    conn.close()

def buscar_y_elegir_direccion(gmaps, consulta, usuario):
    resultados = gmaps.geocode(consulta)
    if not resultados:
        print("No se encontraron resultados.")
        return None
    
    print(f"\n📍 Opciones para {usuario}:")
    for i, r in enumerate(resultados[:5]):
        print(f"{i+1}. {r['formatted_address']}")
    
    while True:
        try:
            eleccion = int(input("Elegí el número de la dirección correcta: "))
            if 1 <= eleccion <= len(resultados[:5]):
                seleccion = resultados[eleccion - 1]
                direccion = seleccion['formatted_address']
                lat = seleccion['geometry']['location']['lat']
                lon = seleccion['geometry']['location']['lng']
                guardar_ubicacion(usuario, direccion, lat, lon)
                print(f"✅ Dirección guardada para {usuario}: {direccion}")
                return
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

def calcular_distancia(gmaps):
    conn = sqlite3.connect("ubicaciones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT lat, lon FROM ubicaciones WHERE usuario = 'vendedor'")
    vendedor = cursor.fetchone()
    cursor.execute("SELECT lat, lon FROM ubicaciones WHERE usuario = 'comprador'")
    comprador = cursor.fetchone()
    conn.close()

    if not vendedor or not comprador:
        print("Faltan ubicaciones guardadas.")
        return

    origen = (vendedor[0], vendedor[1])
    destino = (comprador[0], comprador[1])

    resultado = gmaps.distance_matrix(origins=[origen], destinations=[destino], mode="driving")
    try:
        distancia = resultado['rows'][0]['elements'][0]['distance']['text']
        duracion = resultado['rows'][0]['elements'][0]['duration']['text']
        print("\n📏 Distancia:", distancia)
        print("⏱️ Duración estimada:", duracion)
        return distancia, duracion
    except:
        print("Error calculando distancia.")
        return None, None

def main():
    gmaps = googlemaps.Client(key=API_KEY)
    crear_base()

    for usuario in ["vendedor", "comprador"]:
        consulta = input(f"\n🧭 Ingresá una dirección o referencia para {usuario}: ")
        buscar_y_elegir_direccion(gmaps, consulta, usuario)

    calcular_distancia(gmaps)

if __name__ == "__main__":
    main()
