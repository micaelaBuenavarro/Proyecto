class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

class Producto:
    def __init__(self, nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia, cantidad_de_stock):
        self.nombre = nombre
        self.costo_insumo = costo_insumo
        self.costo_envase = costo_envase
        self.costo_etiqueta = costo_etiqueta
        self.margen_ganancia = margen_ganancia
        self.cantidad_de_stock = cantidad_de_stock

    def calcular_precio(self):
        costo_total = self.costo_insumo + self.costo_envase + self.costo_etiqueta
        precio_venta = costo_total + (costo_total * self.margen_ganancia / 100)
        return precio_venta
    
    def calcular_precio(self):
        cantidad_stock = cantidad_stock
        return cantidad_stock

# Lista para guardar productos cargados
productos = []

# --- AGREGAR PRODUCTOS ---
print("Bienvenido vendedor. Vamos a cargar productos.")
while True:
    nombre = input("Ingrese el nombre del producto (o 'fin' para terminar): ").strip()
    if nombre.lower() == 'fin':
        break
    try:
        costo_insumo = float(input("Costo de insumo: "))
        costo_envase = float(input("Costo del envase: "))
        costo_etiqueta = float(input("Costo de etiqueta: "))
        margen = float(input("Margen de ganancia (%): "))
    except ValueError:
        print("Error: Ingresá valores numéricos válidos.")
        continue

    producto = Producto(nombre, costo_insumo, costo_envase, costo_etiqueta, margen)
    productos.append(producto)
    print(f"Producto '{nombre}' agregado con éxito. Precio de venta: ${producto.calcular_precio():.2f}\n")

# --- MOSTRAR PRODUCTOS ---
print("\nProductos disponibles para comprar:")
for i, producto in enumerate(productos, 1):
    print(f"{i}. {producto.nombre} - Precio: ${producto.calcular_precio():.2f}")

# --- CARRITO DE COMPRAS ---
carrito = {}
for producto in productos:
    while True:
        try:
            cantidad = int(input(f"\n¿Cuántos '{producto.nombre}' deseas comprar? "))
            if cantidad < 0:
                print("Por favor ingresa un número positivo.")
            else:
                carrito[producto] = cantidad
                break
        except ValueError:
            print("Por favor ingresa un número válido.")

# --- CALCULAR TOTAL ---
total = 0
print("\nResumen de tu compra:")
for producto, cantidad in carrito.items():
    precio_unitario = producto.calcular_precio()
    subtotal = precio_unitario * cantidad
    print(f"- {cantidad} x {producto.nombre} = ${subtotal:.2f}")
    total += subtotal

# --- ENVÍO ---
tarifa_km = 50
distancias = {
    "San Rafael (Centro)": 0, "General Alvear": 90, "Malargüe": 189, "Tunuyán": 150,
    "San Carlos": 130, "Tupungato": 182, "La Paz": 250, "Santa Rosa": 205,
    "Junín": 247, "Rivadavia": 244, "San Martín": 250, "Maipú": 225,
    "Godoy Cruz": 228, "Guaymallén": 234, "Luján de Cuyo": 213, "Las Heras": 237,
    "Lavalle": 265, "Cacheuta": 265, "Potrerillos": 241, "El Nihuil": 75,
    "Los Reyunos": 35, "Valle Grande": 35, "El Sosneado": 140, "Las Cuevas": 390,
    "Puente del Inca": 367, "Las Leñas": 430, "Malargüe (otra entrada)": 421,
    "Monte Comán": 56, "Capitán Montoya": 12, "Las Malvinas": 35, "Cuadro Nacional": 3
}

localidad_usuario = input("\n¿En qué localidad de Mendoza vivís? (ej: Tunuyán): ").strip()

if localidad_usuario in distancias:
    km = distancias[localidad_usuario]
    costo_envio = km * tarifa_km
    print(f"\nDistancia desde San Rafael: {km} km")
    print(f"Costo estimado del envío: ${costo_envio:,} ARS")
    total += costo_envio
else:
    print("\nLo siento, no tengo información de esa localidad.")
    costo_envio = 0

print(f"\nTotal a pagar (incluye envío si corresponde): ${total:.2f}")

# --- MÉTODO DE PAGO ---
while True:
    metodo_pago = input("\n¿Deseas pagar con 'efectivo' o 'transferencia'? ").strip().lower()
    if metodo_pago == "transferencia":
        print("\nPor favor realiza la transferencia al siguiente alias:")
        print("👉 alias.tienda.productos")
        print("Una vez recibida la transferencia, se confirmará tu pago.")
        break
    elif metodo_pago == "efectivo":
        while True:
            try:
                billete = float(input("\n¿Con qué billete vas a pagar? $"))
                if billete < total:
                    print("El billete no cubre el total, por favor ingresa uno mayor.")
                else:
                    vuelto = billete - total
                    print(f"\nRecibido: ${billete:.2f}")
                    print(f"Vuelto: ${vuelto:.2f}")
                    break
            except ValueError:
                print("Por favor ingresa un monto válido.")
        break
    else:
        print("Opción no válida. Escribí 'efectivo' o 'transferencia'.")

print("\n¡Gracias por tu compra!")
