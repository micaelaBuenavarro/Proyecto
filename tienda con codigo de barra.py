"""codico completo con codigo de barra"""
print("¡Script iniciado correctamente!")

import sqlite3

class Usuario:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo 

class Producto:
    def __init__(self, nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia, stock, codigo_barra=None):
        self.nombre = nombre
        self.costo_insumo = costo_insumo 
        self.costo_envase = costo_envase 
        self.costo_etiqueta = costo_etiqueta 
        self.margen_ganancia = margen_ganancia 
        self.stock = stock
        self.codigo_barra = codigo_barra

    def calcular_precio(self):  
        costo_total = self.costo_insumo + self.costo_etiqueta + self.costo_envase
        precio_venta = costo_total + (costo_total * self.margen_ganancia / 100)
        return precio_venta

class TiendaVirtual:
    def __init__(self):
        self.productos = [] 
        self.usuarios = []
        self.inicializar_base()
        self.cargar_productos_desde_base()  # Cargar productos al iniciar

    def inicializar_base(self):
        conn = sqlite3.connect('tienda_virtual.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                costo_insumo REAL,
                costo_envase REAL,
                costo_etiqueta REAL,
                margen_ganancia REAL,
                stock INTEGER,
                codigo_barra TEXT UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

    def cargar_productos_desde_base(self):
        self.productos = []  # Vaciar lista antes de cargar
        conn = sqlite3.connect('tienda_virtual.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia, stock, codigo_barra FROM productos")
        filas = cursor.fetchall()
        for fila in filas:
            nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra = fila
            producto = Producto(nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra)
            self.productos.append(producto)
        conn.close()

    def registrar_usuario(self):
        nombre = input("Ingrese nombre de usuario: ")
        for usuario in self.usuarios:
            if nombre == usuario.nombre:
                print("Este usuario ya existe.")
                return

        tipo = input("¿Es 'vendedor' o 'comprador'? ").lower()
        if tipo not in ["vendedor", "comprador"]:
            print("Tipo no válido.")
            return

        self.usuarios.append(Usuario(nombre, tipo))
        print(f"Usuario '{nombre}' registrado como {tipo}.")

    def login(self):
        nombre = input("Ingrese su nombre de usuario: ")
        for usuario in self.usuarios:
            if nombre == usuario.nombre:
                return usuario
        print("Usuario no encontrado")
        return None

    def agregar_producto(self):
        conn = sqlite3.connect('tienda_virtual.db')
        cursor = conn.cursor()

        print("\n¿Querés agregar un producto manualmente o escaneando código de barras?")
        metodo = input("Escribí 'manual' o 'escanear': ").strip().lower()

        if metodo == "escanear":
            codigo_barra = input("Escaneá o ingresá el código de barras: ").strip()
            cursor.execute("SELECT nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia, stock FROM productos WHERE codigo_barra = ?", (codigo_barra,))
            resultado = cursor.fetchone()

            if resultado:
                nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock = resultado
                producto = Producto(nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra)
                self.productos.append(producto)
                print(f"Producto '{nombre}' cargado desde la base de datos.")
                print(f"Precio de venta: ${producto.calcular_precio():.2f}")
            else:
                print("Código no encontrado. Ingresá los datos manualmente:")
                nombre = input("Nombre del producto: ")
                costo_insumo = float(input("Costo de insumo: "))
                costo_envase = float(input("Costo del envase: "))
                costo_etiqueta = float(input("Costo de etiqueta: "))
                margen = float(input("Margen de ganancia (%): "))
                stock = int(input("Stock inicial: "))

                # Insertar producto nuevo en la base
                cursor.execute("""
                    INSERT INTO productos (nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia, stock, codigo_barra)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra))
                conn.commit()

                producto = Producto(nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra)
                self.productos.append(producto)
                print(f"Producto '{nombre}' agregado y guardado.")
                print(f"Precio de venta: ${producto.calcular_precio():.2f}")

        elif metodo == "manual":
            nombre = input("Nombre del producto: ")
            costo_insumo = float(input("Costo de insumo: "))
            costo_envase = float(input("Costo del envase: "))
            costo_etiqueta = float(input("Costo de etiqueta: "))
            margen = float(input("Margen de ganancia (%): "))
            stock = int(input("Stock inicial: "))
            codigo_barra = input("Código de barras (opcional): ").strip()

            # Verificar si el código de barras ya existe
            if codigo_barra:
                cursor.execute("SELECT id FROM productos WHERE codigo_barra = ?", (codigo_barra,))
                if cursor.fetchone():
                    print("El código de barras ya existe. No se puede agregar el producto.")
                    conn.close()
                    return

            # Insertar producto
            cursor.execute("""
                INSERT INTO productos (nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia, stock, codigo_barra)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra if codigo_barra else None))
            conn.commit()

            producto = Producto(nombre, costo_insumo, costo_envase, costo_etiqueta, margen, stock, codigo_barra if codigo_barra else None)
            self.productos.append(producto)
            print(f"Producto '{nombre}' agregado.")
            print(f"Precio de venta: ${producto.calcular_precio():.2f}")

        else:
            print("Opción inválida.")

        conn.close()

    def mostrar_productos(self):
        self.cargar_productos_desde_base()  # Asegura la lista sincronizada con la base
        if not self.productos:
            print("No hay productos disponibles.")
            return
        for i, producto in enumerate(self.productos, 1):
            cod_barra = producto.codigo_barra if producto.codigo_barra else "N/A"
            print(f"{i}. {producto.nombre} - Precio: ${producto.calcular_precio():.2f} - Stock: {producto.stock} unidades - Código de barras: {cod_barra}")

def main():
    tienda = TiendaVirtual()

    while True:
        print("\n___Menú Principal___")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            tienda.registrar_usuario()

        elif opcion == "2":
            usuario = tienda.login()
            if usuario:
                if usuario.tipo == "vendedor":
                    while True:
                        print("\n___Menú Vendedor___")
                        print("1. Agregar producto")
                        print("2. Ver productos")
                        print("3. Cerrar sesión")
                        op = input("Opción: ")

                        if op == "1":
                            tienda.agregar_producto()
                        elif op == "2":
                            tienda.mostrar_productos()
                        elif op == "3":
                            break
                        else:
                            print("Opción inválida.")

                elif usuario.tipo == "comprador":
                    carrito = {}
                    total = 0
                    while True:
                        print("\n___Menú Comprador___")
                        print("1. Ver productos")
                        print("2. Comprar")
                        print("3. Cerrar sesión")
                        op = input("Opción: ")

                        if op == "1":
                            tienda.mostrar_productos()

                        elif op == "2":
                            while True:
                                tienda.mostrar_productos()
                                if not tienda.productos:
                                    break

                                try:
                                    eleccion = input("\nIngrese el número del producto que desea comprar (o '0' para finalizar): ")
                                    if eleccion == '0':
                                        break
                                    eleccion = int(eleccion)
                                    if eleccion < 1 or eleccion > len(tienda.productos):
                                        print("Número inválido.")
                                        continue

                                    producto = tienda.productos[eleccion - 1]
                                    print(f"Elegiste: {producto.nombre} (Stock: {producto.stock})")

                                    cantidad = int(input(f"¿Cuántas unidades de '{producto.nombre}' deseas comprar? "))
                                    if cantidad <= 0:
                                        print("Cantidad inválida.")
                                        continue
                                    if cantidad > producto.stock:
                                        print(f"No hay suficiente stock. Solo quedan {producto.stock} unidades.")
                                        continue

                                    if producto in carrito:
                                        carrito[producto] += cantidad
                                    else:
                                        carrito[producto] = cantidad

                                    print(f"{cantidad} unidad(es) de {producto.nombre} agregadas al carrito.")

                                except ValueError:
                                    print("Entrada inválida. Intenta nuevamente.")
                            
                            if not carrito:
                                print("No se agregaron productos al carrito.")
                                continue

                            # Calcular total
                            for producto, cantidad in carrito.items():
                                producto.stock -= cantidad
                                precio_unitario = producto.calcular_precio()
                                subtotal = precio_unitario * cantidad
                                print(f"- {cantidad} x {producto.nombre} = ${subtotal:.2f}")
                                total += subtotal

                            # Envío
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
                                print("Localidad no encontrada. El envío no será calculado.")

                            print("\nStock actualizado:")
                            for producto in tienda.productos:
                                print(f"{producto.nombre}: {producto.stock} unidades")

                            print(f"\nTotal a pagar (incluye envío si corresponde): ${total:.2f}")

                            # Método de pago
                            while True:
                                metodo_pago = input("\n¿Deseas pagar con 'efectivo' o 'transferencia'? ").strip().lower()
                                if metodo_pago == "transferencia":
                                    print("\nPor favor realiza la transferencia al siguiente alias:")
                                    print("👉 alias.tienda.productos")
                                    break
                                elif metodo_pago == "efectivo":
                                    while True:
                                        try:
                                            billete = float(input("¿Con qué billete vas a pagar? $"))
                                            if billete < total:
                                                print("El billete no cubre el total.")
                                            else:
                                                vuelto = billete - total
                                                print(f"Recibido: ${billete:.2f} | Vuelto: ${vuelto:.2f}")
                                                break
                                        except ValueError:
                                            print("Monto inválido.")
                                    break
                                else:
                                    print("Opción no válida. Escribí 'efectivo' o 'transferencia'.")

                            print("\n¡Gracias por tu compra!")
                            carrito = {}
                            total = 0

        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
