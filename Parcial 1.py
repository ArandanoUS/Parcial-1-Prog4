import redis
import uuid

# Configuración de conexión a KeyDB
KEYDB_HOST = "localhost"
KEYDB_PORT = 6379
KEYDB_DB = 0

keydb = redis.StrictRedis(host=KEYDB_HOST, port=KEYDB_PORT, db=KEYDB_DB, decode_responses=True)

# Funciones CRUD para el sistema de registro de presupuesto
def registrar_articulo():
    """Registrar un nuevo artículo en el presupuesto."""
    try:
        id_articulo = str(uuid.uuid4())  # Genera un ID único
        descripcion = input("Descripción del artículo: ")
        cantidad = input("Cantidad (en números): ")
        categoria = input("Categoría del artículo: ")

        # Validar entrada
        if not descripcion or not cantidad.isdigit() or not categoria:
            print("❌ Entrada inválida. Por favor, asegúrese de ingresar valores correctos.")
            return

        # Crear el hash en KeyDB
        keydb.hset(
            id_articulo,
            mapping={
                "descripcion": descripcion,
                "cantidad": cantidad,
                "categoria": categoria,
            }
        )
        print(f"✅ Artículo registrado exitosamente con ID: {id_articulo}")
    except Exception as e:
        print(f"❌ Error al registrar el artículo: {e}")

def buscar_articulo():
    """Buscar un artículo en el presupuesto por ID."""
    try:
        id_articulo = input("Ingrese el ID del artículo a buscar: ")
        if not keydb.exists(id_articulo):
            print("❌ No se encontró un artículo con ese ID.")
            return

        articulo = keydb.hgetall(id_articulo)
        print("\n📋 Detalles del artículo:")
        print(f"ID: {id_articulo}")
        print(f"Descripción: {articulo['descripcion']}")
        print(f"Cantidad: {articulo['cantidad']}")
        print(f"Categoría: {articulo['categoria']}")
    except Exception as e:
        print(f"❌ Error al buscar el artículo: {e}")

def editar_articulo():
    """Editar un artículo existente en el presupuesto."""
    try:
        id_articulo = input("Ingrese el ID del artículo a editar: ")
        if not keydb.exists(id_articulo):
            print("❌ No se encontró un artículo con ese ID.")
            return

        articulo = keydb.hgetall(id_articulo)
        print("\n📋 Detalles actuales del artículo:")
        print(f"Descripción: {articulo['descripcion']}")
        print(f"Cantidad: {articulo['cantidad']}")
        print(f"Categoría: {articulo['categoria']}")

        nueva_descripcion = input("Nueva descripción (dejar en blanco para no cambiar): ")
        nueva_cantidad = input("Nueva cantidad (dejar en blanco para no cambiar): ")
        nueva_categoria = input("Nueva categoría (dejar en blanco para no cambiar): ")

        # Actualizar sólo los campos que se hayan proporcionado
        if nueva_descripcion:
            keydb.hset(id_articulo, "descripcion", nueva_descripcion)
        if nueva_cantidad and nueva_cantidad.isdigit():
            keydb.hset(id_articulo, "cantidad", nueva_cantidad)
        if nueva_categoria:
            keydb.hset(id_articulo, "categoria", nueva_categoria)

        print("✅ Artículo actualizado exitosamente.")
    except Exception as e:
        print(f"❌ Error al editar el artículo: {e}")

def eliminar_articulo():
    """Eliminar un artículo del presupuesto."""
    try:
        id_articulo = input("Ingrese el ID del artículo a eliminar: ")
        if not keydb.exists(id_articulo):
            print("❌ No se encontró un artículo con ese ID.")
            return

        keydb.delete(id_articulo)
        print("✅ Artículo eliminado exitosamente.")
    except Exception as e:
        print(f"❌ Error al eliminar el artículo: {e}")

def ver_listado_articulos():
    """Ver el listado de todos los artículos en el presupuesto."""
    try:
        claves = keydb.keys()
        if not claves:
            print("❌ No hay artículos registrados.")
            return

        print("\n📜 Listado de artículos:")
        for i, clave in enumerate(claves, start=1):
            articulo = keydb.hgetall(clave)
            print(f"{i}. ID: {clave}, Descripción: {articulo['descripcion']}, Cantidad: {articulo['cantidad']}, Categoría: {articulo['categoria']}")
    except Exception as e:
        print(f"❌ Error al mostrar el listado de artículos: {e}")

# Menú principal
def menu():
    """Mostrar el menú principal del sistema."""
    while True:
        print("\n=== Sistema de Registro de Presupuesto ===")
        print("1. Registrar nuevo artículo")
        print("2. Buscar artículo por ID")
        print("3. Editar artículo existente")
        print("4. Eliminar artículo existente")
        print("5. Ver listado de artículos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_articulo()
        elif opcion == "2":
            buscar_articulo()
        elif opcion == "3":
            editar_articulo()
        elif opcion == "4":
            eliminar_articulo()
        elif opcion == "5":
            ver_listado_articulos()
        elif opcion == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()