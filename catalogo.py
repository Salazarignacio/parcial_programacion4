from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen = True)
class UnidadMedida:
    nombre:str
    simbolo :str
    tipo :str
    

class Categoria:
    def __init__(self, nombre: str, descripcion: str = "Sin descripcion"):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoria no puede estar vacia")
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self):
        return self._nombre
    @property
    def descripcion(self):
        return self._descripcion

class ProductoCategoria():
    def __init__(self, categoria : Categoria, es_principal : bool ):
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self):
        return self._categoria

    @property
    def es_principal(self):
        return self._es_principal
    
    def marcar_principal(self, valor: bool):
        self._es_principal = valor


class Producto(ABC):
    def __init__(self, nombre: str, precio_base: float, stock_cantidad: float, habilitado : bool, categoria : Categoria, unidad_venta: UnidadMedida | None = None ):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = nombre
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")
        self._precio_base = precio_base
        if stock_cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")
        self._stock_cantidad = stock_cantidad
        self._habilitado = habilitado
        self._unidad_venta = unidad_venta
        self._clasificaciones : list[ProductoCategoria] = []
        self.clasificar_en(categoria, True)
    @property
    def nombre(self)-> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self)-> UnidadMedida:
        return self._unidad_venta

    @property
    def disponible(self)-> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        pass

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        raise NotImplementedError

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None:
        categoriaCreada : ProductoCategoria = ProductoCategoria(categoria, es_principal)
        self._clasificaciones.append(categoriaCreada)

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for productoCategoria in self._clasificaciones:
            if(productoCategoria.es_principal):
                return productoCategoria.categoria

    def exportar(self) -> str:
        return None

class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        return cantidad * self.precio_base

class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        return cantidad * self.precio_base

class ProductoCombo(Producto):
    def __init__(self, nombre: str,componentes: list[Producto] , categoria : Categoria, descuento: float ):
            precio_base = 0 
            stock_cantidad = 0 
            habilitado = True 
            for componente in componentes:
                precio_base += componente.precio_final(1)
                stock_cantidad = componente._stock_cantidad
                if(not componente.disponible):
                    habilitado = False
            super().__init__(nombre, precio_base, stock_cantidad,  habilitado, categoria)
            self._componentes = componentes 
            self._descuento = descuento
    
    def precio_final(self, cantidad: float) -> float:
            return self.precio_base * cantidad

class Exportable(Protocol):
    def exportar(self) -> str:
        ...


categoria1 = Categoria("Lacteos", "productos hechos con lache")
categoria2 = Categoria("BBlanco", "productos hechos con lache")
producto1 = ProductoSimple("lechita", 1200, 30, True, categoria1)
producto2 = ProductoSimple("queso", 100, 30, True, categoria1)
combo = ProductoCombo("Combo loco", [producto1, producto2], categoria1, 10)
print(producto1.nombre)
print(combo.precio_base)
for p_categoria in producto1.categorias():
    print(p_categoria.categoria.nombre)
print(producto1.categoria_principal().nombre)
producto1.clasificar_en(categoria2, True)