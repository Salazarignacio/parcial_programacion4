from catalogo import (
    UnidadMedida,
    Categoria,
    Producto,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    ProductoDestacado,
    exportar_catalogo,
)
import libreria_externa


def main():
    print("=== DEMO PARCIAL POO - FOOD STORE ===\n")

    # 1. Categorias y unidades de medida
    categoria_lacteos = Categoria("Lacteos", "Productos derivados de la leche")
    categoria_bebidas = Categoria("Bebidas", "Productos bebibles")
    categoria_bebidas_alcoholicas = Categoria("Con Alcohol")
    categoria_fiambres = Categoria("Fiambres")
    categoria_almacen = Categoria("Almacen")

    kilogramos = UnidadMedida("Kilogramos", "kg", "masa")
    litros = UnidadMedida("Litros", "L", "volumen")

    # 2. Componentes que se van a usar en el combo
    queso = ProductoPorPeso("Queso Tybo", 11500.00, 5, True, categoria_lacteos, kilogramos)
    jamon = ProductoPorPeso("Jamon Cocido", 15300.00, 8, True, categoria_fiambres, kilogramos)

    # 3. Productos del catalogo (al menos 4 sin contar queso y jamon que son componentes)
    leche = ProductoSimple("Leche Descremada", 2200.00, 50, True, categoria_lacteos, litros)
    pan = ProductoSimple("Pan Lactal", 2500.00, 20, True, categoria_almacen)  # Sin unidad de medida
    vino_malbec = ProductoSimple("El Enemigo", 18500.00, 12, True, categoria_bebidas_alcoholicas)
    asado = ProductoPorPeso("Asado de Tira", 9800.00, 15, True, categoria_fiambres, kilogramos)
    combo_picada = ProductoCombo("Combo Picada", [queso, jamon], categoria_fiambres, 0.15)

    # Clasificacion secundaria
    vino_malbec.clasificar_en(categoria_bebidas, es_principal=False)

    # Lista con los productos del catalogo
    catalogo = [leche, pan, vino_malbec, asado, combo_picada]

    # 4. Mostrar el catalogo y calcular precios finales
    print("--- CATALOGO DE PRODUCTOS ---")
    for prod in catalogo:
        print(f"Producto: {prod.nombre} ({prod.__class__.__name__})")
        print(f"  Categoria principal: {prod.categoria_principal().nombre}")
        categorias_nombres = [c.categoria.nombre for c in prod.categorias()]
        print(f"  Todas las categorias: {', '.join(categorias_nombres)}")
        print(f"  Precio publicado: {prod.precio_publicado}")
        print(f"  Disponible: {prod.disponible}")

    print("\n--- PRUEBA DE PRECIOS FINALES ---")
    print("Precio de 3 leches:", leche.precio_final(3))
    print("Precio de 0.5 kg de asado:", asado.precio_final(0.5))
    print("Precio de 2 combos de picada:", combo_picada.precio_final(2))

    # 5. Exportar catalogo con FichaPuntoDeVenta (Protocol)
    print("\n--- EXPORTACION AL PUNTO DE VENTA ---")
    ficha = libreria_externa.FichaPuntoDeVenta("101", "Caja Principal")
    items_a_exportar = [leche, asado, combo_picada, ficha]
    exportados = exportar_catalogo(items_a_exportar)
    for linea in exportados:
        print("Exportado:", linea)

    # 6. Demostraciones de decisiones de diseno para la defensa
    print("\n--- DECISIONES DE DISENO ---")

    # A. Falla temprana: no se puede instanciar la clase abstracta
    print("\n* Probando falla temprana:")
    try:
        Producto("Invalido", 1000, 10, True, categoria_almacen)
    except TypeError as e:
        print("  Correcto, falla al instanciar Producto abstracto:", e)

    class ProductoIncompleto(Producto):
        pass

    try:
        ProductoIncompleto("Incompleto", 1000, 10, True, categoria_almacen)
    except TypeError as e:
        print("  Correcto, falla al instanciar subclase sin precio_final():", e)

    # B. Composicion: ProductoCategoria se crea adentro y no se puede mutar desde afuera
    print("\n* Probando composicion (ProductoCategoria):")
    vino_malbec.clasificar_en(categoria_almacen, es_principal=True)
    print("  Nueva categoria principal tras reclasificar:", vino_malbec.categoria_principal().nombre)
    try:
        vino_malbec.categorias().append("categoria extra")
    except AttributeError:
        print("  Correcto, categorias() devuelve una tupla inmutable")

    # C. Agregacion: los componentes sobreviven al combo y se pueden volver a agrupar
    print("\n* Probando agregacion (ProductoCombo):")
    print(f"  Componentes '{queso.nombre}' y '{jamon.nombre}' existen independientemente del combo")
    combo_sandwich = ProductoCombo("Combo Sandwich", [queso, jamon], categoria_fiambres, 0.10)
    print(f"  Se reagruparon en otro combo nuevo: '{combo_sandwich.nombre}'")

    # D. ProductoDestacado (agregacion con Producto)
    print("\n* Probando ProductoDestacado:")
    destacado = ProductoDestacado(vino_malbec, orden=1)
    print(f"  Producto destacado: {destacado.producto.nombre}, orden en vidriera: {destacado.orden_vidriera}")

    # E. Encapsulamiento y disponibilidad
    print("\n* Probando habilitar y deshabilitar:")
    print("  Leche disponible:", leche.disponible)
    leche.deshabilitar()
    print("  Leche tras deshabilitar:", leche.disponible)
    leche.habilitar()
    print("  Leche tras habilitar:", leche.disponible)


if __name__ == "__main__":
    main()
