"""
Demostracion ejecutable del catalogo de Food Store (Requerimiento 5).

Consigna:
Un script que arme un catalogo con al menos 4 productos —sin contar los componentes de un combo—,
cubriendo las tres subclases de venta (ProductoSimple, ProductoPorPeso y ProductoCombo), los clasifique en
categorias, asigne unidades de venta distintas, calcule precios finales con cantidades distintas, exporte todo junto
con una FichaPuntoDeVenta y muestre el catalogo por consola.

Aprovecha el demo para dejar a la vista las decisiones de diseno:
- que un ProductoCategoria solo puede nacer dentro del producto que lo clasifica —el codigo cliente no lo
  construye, no lo recibe de clasificar_en() y no puede reemplazarlo— (composicion);
- que los componentes si sobreviven al combo, y se los puede volver a agrupar en otro (agregacion);
- que instanciar un Producto abstracto sin precio_final() revienta al construir (falla temprana).
"""

from catalogo import (
    UnidadMedida,
    Categoria,
    Producto,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    ProductoDestacado,
    Exportable,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta


def main() -> None:
    print("=" * 75)
    print("        DEMO DEL SISTEMA DE CATALOGO - FOOD STORE (PARCIAL 1 POO)")
    print("=" * 75)

    # =========================================================================
    # 1. DEFINICION DE CATEGORIAS Y UNIDADES DE MEDIDA
    # =========================================================================
    print("\n--- 1. DEFINICION DE CATEGORIAS Y UNIDADES DE MEDIDA ---")

    cat_lacteos = Categoria("Lacteos", "Productos derivados de la leche")
    cat_almacen = Categoria("Almacen", "Provisiones y comestibles generales")
    cat_bebidas = Categoria("Bebidas", "Bebidas generales con y sin alcohol")
    cat_vinos = Categoria("Vinos", "Vinos tintos, blancos y espumantes")
    cat_fiambreria = Categoria("Fiambreria", "Fiambres, quesos y embutidos")
    cat_ofertas = Categoria("Ofertas", "Combos y promociones especiales de la semana")

    u_kg = UnidadMedida("Kilogramo", "kg", "masa")
    u_litro = UnidadMedida("Litro", "L", "volumen")

    print(f"Categorias creadas: {cat_lacteos.nombre}, {cat_almacen.nombre}, {cat_bebidas.nombre}, {cat_vinos.nombre}, {cat_fiambreria.nombre}, {cat_ofertas.nombre}")
    print(f"Unidades de medida inmutables: {u_kg.nombre} ({u_kg.simbolo}), {u_litro.nombre} ({u_litro.simbolo})")

    # =========================================================================
    # 2. CREACION DE PRODUCTOS Y ARMADO DEL CATALOGO
    # =========================================================================
    print("\n--- 2. CREACION DE PRODUCTOS Y COMPONENTES ---")

    # Componentes que se usaran en combos (no cuentan en los 4 requeridos)
    queso_tybo = ProductoPorPeso("Queso Tybo en Barra", 11500.00, 8.0, True, cat_fiambreria, u_kg)
    salame_picado = ProductoPorPeso("Salame Fino Casero", 13800.00, 6.0, True, cat_fiambreria, u_kg)

    # Catalogo principal: al menos 4 productos sin contar los componentes de combo
    # 1. ProductoSimple con unidad de medida (volumen)
    leche = ProductoSimple("Leche Entera Seleccion 1L", 1850.00, 45.0, True, cat_lacteos, u_litro)

    # 2. ProductoSimple sin unidad de medida (por unidad / pieza)
    pan_campo = ProductoSimple("Pan de Campo Artesanal", 2400.00, 20.0, True, cat_almacen, None)

    # 3. ProductoSimple con clasificacion adicional
    vino_malbec = ProductoSimple("Vino Malbec Reserva 750ml", 8900.00, 15.0, True, cat_vinos, None)
    vino_malbec.clasificar_en(cat_bebidas, es_principal=False)

    # 4. ProductoPorPeso para el catalogo
    jamon_crudo = ProductoPorPeso("Jamon Crudo Serrano", 22500.00, 4.5, True, cat_fiambreria, u_kg)

    # 5. ProductoCombo (agrupa queso_tybo y salame_picado con 15% de descuento)
    combo_picada = ProductoCombo("Combo Picada Clasica", [queso_tybo, salame_picado], cat_ofertas, 0.15)

    # Lista de productos que forman el catalogo activo
    catalogo: list[Producto] = [leche, pan_campo, vino_malbec, jamon_crudo, combo_picada]

    print(f"Catalogo cargado con {len(catalogo)} productos principales (cubriendo las 3 subclases de venta).")

    # =========================================================================
    # 3. MUESTRA DEL CATALOGO POR CONSOLA Y CALCULO POLIMORFICO DE PRECIOS
    # =========================================================================
    print("\n--- 3. MUESTRA DETALLADA DEL CATALOGO ---")

    # Cantidades de prueba para cada producto
    cantidades_prueba = {
        leche: 3.0,          # 3 botellas
        pan_campo: 2.0,      # 2 panes
        vino_malbec: 1.0,    # 1 botella
        jamon_crudo: 0.35,   # 350 gramos
        combo_picada: 2.0,   # 2 combos
    }

    for prod in catalogo:
        cat_principal = prod.categoria_principal().nombre
        todas_cats = [c.categoria.nombre for c in prod.categorias()]
        cant = cantidades_prueba[prod]
        precio_calc = prod.precio_final(cant)

        print(f"\n* Producto: {prod.nombre}")
        print(f"  - Tipo de clase: {prod.__class__.__name__}")
        print(f"  - Categoria Principal: {cat_principal}")
        print(f"  - Todas las Clasificaciones: {', '.join(todas_cats)}")
        print(f"  - Precio Publicado: {prod.precio_publicado}")
        print(f"  - Stock Disponible: {prod.disponible} (Stock: {prod._stock_cantidad})")
        print(f"  - Calculo de precio_final({cant}): $ {precio_calc:.2f}")

    # =========================================================================
    # 4. EXPORTACION CONJUNTA CON FICHA EXTERNA (REQUERIMIENTO 4 - PROTOCOL)
    # =========================================================================
    print("\n" + "=" * 75)
    print("--- 4. EXPORTACION AL PUNTO DE VENTA (Exportable Protocol) ---")
    print("=" * 75)

    # Ficha externa provista por el tercero (libreria_externa.py)
    ficha_pos = FichaPuntoDeVenta("POS-8890", "Ficha Caja Registradora - Sucursal Centro")

    # Lista polimorfica que agrupa productos del dominio y fichas externas bajo el Protocol Exportable
    items_exportables: list[Exportable] = [*catalogo, ficha_pos]

    lineas_exportadas = exportar_catalogo(items_exportables)
    print(f"Total de registros exportados: {len(lineas_exportadas)}")
    for linea in lineas_exportadas:
        print(f"  -> {linea}")

    # =========================================================================
    # 5. DEMOSTRACION DE DECISIONES DE DISENO
    # =========================================================================
    print("\n" + "=" * 75)
    print("--- 5. EVIDENCIA DE DECISIONES DE DISENO ---")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # A. Falla temprana: Instanciar clase abstracta o subclase incompleta
    # -------------------------------------------------------------------------
    print("\n[A] Falla Temprana (Herencia y ABC):")
    try:
        Producto("Producto Abstracto", 1000.0, 10.0, True, cat_almacen)
    except TypeError as e:
        print(f"  [OK] Instanciar Producto directo falla al construir: {e}")

    class SubclaseIncompleta(Producto):
        pass  # No implementa precio_final()

    try:
        SubclaseIncompleta("Incompleto", 1000.0, 5.0, True, cat_almacen)
    except TypeError as e:
        print(f"  [OK] Instanciar subclase sin precio_final() falla al construir: {e}")

    # -------------------------------------------------------------------------
    # B. Composicion: Producto y ProductoCategoria
    # -------------------------------------------------------------------------
    print("\n[B] Composicion (Producto -> ProductoCategoria):")
    # 1. clasificar_en() fabrica internamente el vinculo y no lo devuelve
    res_clasif = pan_campo.clasificar_en(cat_ofertas, es_principal=False)
    print(f"  [OK] clasificar_en() retorna: {res_clasif} (el cliente nunca recibe ni instancia el vinculo)")

    # 2. categorias() devuelve una tupla inmutable (copia protegida)
    tupla_cats = pan_campo.categorias()
    try:
        tupla_cats.append("Intento hack")  # type: ignore
    except AttributeError:
        print("  [OK] categorias() es tupla inmutable: append() lanza AttributeError.")

    # 3. Invariante de unica categoria principal al reclasificar
    print(f"  - Principal actual de Pan de Campo: {pan_campo.categoria_principal().nombre}")
    pan_campo.clasificar_en(cat_lacteos, es_principal=True)
    print(f"  - Nueva principal tras reclasificar con es_principal=True: {pan_campo.categoria_principal().nombre}")
    principales = [c for c in pan_campo.categorias() if c.es_principal]
    print(f"  [OK] Cantidad de clasificaciones principales en todo momento: {len(principales)}")

    # 4. Clasificar dos veces en la misma categoria lanza excepcion de dominio
    try:
        pan_campo.clasificar_en(cat_almacen)
    except ValueError as e:
        print(f"  [OK] Clasificar dos veces en la misma categoria lanza ValueError: {e}")

    # -------------------------------------------------------------------------
    # C. Agregacion: ProductoCombo y sus componentes
    # -------------------------------------------------------------------------
    print("\n[C] Agregacion (ProductoCombo -> Producto):")
    print(f"  - Componentes del combo existen antes de crearlo: '{queso_tybo.nombre}' y '{salame_picado.nombre}'")
    print(f"  - Se pueden reutilizar en otro combo independiente:")
    combo_degustacion = ProductoCombo(
        "Combo Degustacion Gourmet",
        [queso_tybo, jamon_crudo],
        cat_ofertas,
        0.10
    )
    print(f"    Nuevo combo creado: '{combo_degustacion.nombre}' con componentes: {[c.nombre for c in combo_degustacion.componentes]}")
    
    # Destruir el primer combo y demostrar que los componentes siguen vivos
    del combo_picada
    print(f"  [OK] Tras eliminar combo_picada, '{queso_tybo.nombre}' sigue existiendo con precio: $ {queso_tybo.precio_base:.2f}")

    # -------------------------------------------------------------------------
    # D. Requerimiento 3: ProductoDestacado como Agregacion
    # -------------------------------------------------------------------------
    print("\n[D] Decision ProductoDestacado (Agregacion con Producto):")
    # Puede destacar un ProductoSimple
    destacado_vino = ProductoDestacado(vino_malbec, orden=1)
    # Puede destacar un ProductoCombo
    destacado_combo = ProductoDestacado(combo_degustacion, orden=2)

    print(f"  - Destacado 1: {destacado_vino.producto.nombre} (Orden vidriera: {destacado_vino.orden_vidriera})")
    print(f"  - Destacado 2: {destacado_combo.producto.nombre} (Orden vidriera: {destacado_combo.orden_vidriera})")
    print("  [OK] Cualquier tipo de producto se destaca sin herencia multiple ni alterar la jerarquia.")

    # -------------------------------------------------------------------------
    # E. Encapsulamiento y Disponibilidad (habilitar / deshabilitar)
    # -------------------------------------------------------------------------
    print("\n[E] Encapsulamiento y Disponibilidad:")
    print(f"  - Leche disponible inicialmente: {leche.disponible}")
    leche.deshabilitar()
    print(f"  - Leche tras deshabilitar(): {leche.disponible} (stock={leche._stock_cantidad}, habilitado={leche._habilitado})")
    leche.habilitar()
    print(f"  - Leche tras habilitar(): {leche.disponible}")

    print("\n" + "=" * 75)
    print("              FIN DE LA DEMOSTRACION EXITOSA")
    print("=" * 75)


if __name__ == "__main__":
    main()
