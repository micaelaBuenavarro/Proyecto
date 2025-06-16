class Usuario: 
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo 

class Producto: 
    
    def __init__(self, nombre, costo_insumo, costo_envase, costo_etiqueta, margen_ganancia):
        self.nombre = nombre
        self.costo_insumo = costo_insumo 
        self.costo_envase = costo_envase 
        self.costo_etiqueta = costo_etiqueta 
        self.margen_ganancia = margen_ganancia 

    def calcular_precio(self):  
        costo_total = self.costo_insumo + self.costo_etiqueta + self.costo_envase
        precio_venta = costo_total + (costo_total * self.margen_ganancia / 100)
        return precio_venta

    def mostrar_productos(self):
        for producto in self.producto.values():
            print(f"nombre:{producto.nombre}")
            print(f"precio de venta: ${producto.calcular_precio():.2}")
        

class TiendaVirtual:
    
    def __init__(self):
        self.productos = {} 
        self.usuarios =[]
        
    def registrar_usuario(self):
       nombre = input("ingrese nombre de usuario: ")
       for usuario in self.usuarios:
           if nombre in self.usuarios:
                print("Este usuario ya existe. ")
                return
       tipo = input("¿Es 'vendedor' o 'comprador'? ").lower()
       if tipo not in ["vendedor", "comprador"]:
            print("tipo no valido.")
            return
        
       self.usuarios.append(Usuario(nombre, tipo))
       print(f"usuario '{nombre}' registrado como {tipo}.")
    
    def login(self):
        nombre =input("ingrese su nombre de usuario. ")
        
        for usuario in self.usuarios:
            if nombre == usuario.nombre:
                return usuario
            
        
        print("usuario no encontrado.")
        return None

    def agregar_producto(self):
        nombre = input("Ingrese el nombre del producto: ")
        costo_insumo = float(input("Costo de insumo: "))
        costo_envase = float(input("Costo del envase: "))
        costo_etiqueta = float(input("Costo de etiqueta: "))
        margen = float(input("Margen de ganancia (%): "))
    
        producto = Producto(nombre, costo_insumo, costo_envase, costo_etiqueta, margen)
        self.productos[nombre] = producto
    
        print(f"Producto '{nombre}' agregado con éxito.")
        print(f"Precio de venta: ${producto.calcular_precio():.2f}")
    
    def mostrar_productos(self):
        if not self.productos:
            print("No hay productos disponibles.")
            return
        for producto in self.productos.values():
            print(f"Producto: {producto.nombre}")
            print(f"Precio de venta: ${producto.calcular_precio():.2f}")
            print("-" * 30)
        
presios = {}

def main():  """main = crea un objeto en este caso la tienda virtual """
tienda = TiendaVirtual()

while True:
    print("/n___Menu principal___")
    print("1. registrar usuario")
    print("2. iniciar sesión")
    print("3. salir")
    opcion = input ("ingrese su opción: ")
    
    if opcion == "1":
        tienda.registrar_usuario()
        
    elif opcion == "2":
        usuario = tienda.login()
        if usuario:
            if usuario.tipo == "vendedor":
                while True:
                    print("/n___Menú Productos___")
                    print("1. agregar producto")
                    print("2. ver productos")
                    print("3. cerrar sesion")
                    op = input("opción: ")
                    
                    if op == "1":
                        tienda.agregar_producto()
                    elif op == "2":
                        tienda.mostrar_productos()
                    elif op == "3":
                        break 
                    else:
                        print("opcion inválida. ")
                
            elif usuario.tipo == "comprador":
                while True:
                    print("/n___Menu Productos___")
                    print("1. ver productos")
                    print("2. cerrar sesion")
                    op = input("opcion: ")
                
                    if op == "1":
                        tienda.mostrar_productos()
                    elif op == "2":
                        break 
                    else:
                        print("opcion invalida. ")
    elif opcion == "3":
        print("CHAU")
        break
    else:
        print("opcion invalida.")   
         
if __name__ == "__main__":
    main()