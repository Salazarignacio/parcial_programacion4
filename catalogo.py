from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
import libreria_externa

@dataclass(frozen = True)
class UnidadMedida:
    nombre:str
    simbolo :str
    tipo :str
    

class Categoria:
    def __init__(self, nombre: str, descripcion: str = ""):
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
        if (self.unidad_venta):
            return f"$ {self.precio_base:.2f} / {self.unidad_venta.simbolo}"
        else:
            return f"$ {self.precio_base:.2f}"

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        raise NotImplementedError

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None:            
        for clasificacion in self._clasificaciones:
            if (categoria.nombre == clasificacion.categoria.nombre):
                raise ValueError("La categoria ya esta clasificada")

        if(es_principal):
            for clasificacion in self._clasificaciones:
                if(clasificacion.es_principal):
                    clasificacion.marcar_principal(False)
        categoriaCreada : ProductoCategoria = ProductoCategoria(categoria, es_principal)
        self._clasificaciones.append(categoriaCreada)


    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for productoCategoria in self._clasificaciones:
            if(productoCategoria.es_principal):
                return productoCategoria.categoria

    def exportar(self) -> str:
        return f"{self.nombre} + {self.precio_publicado}"

class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        cantidad = float(cantidad)
        if (not (cantidad).is_integer() or cantidad < 1):
            raise ValueError("La cantidad debe ser un numero entero mayor que 0")
        return cantidad * self.precio_base

class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        if (cantidad <= 0):
            raise ValueError("La cantidad debe ser un numero mayor a 0")
        
        return round(cantidad * self.precio_base, 2)

class ProductoCombo(Producto):
    def __init__(self, nombre: str,componentes: list[Producto] , categoria : Categoria, descuento: float ):        
            if(len(componentes) < 2):
                raise ValueError("El combo debe tener al menos 2 productos")
            precio_base = 0 
            stock_cantidad = componentes[0]._stock_cantidad 
            habilitado = True 
        
            for componente in componentes:
                precio_base += componente.precio_final(1)
                stock_cantidad = componente._stock_cantidad if componente._stock_cantidad < stock_cantidad else stock_cantidad
                if(not componente.disponible):
                    habilitado = False

            super().__init__(nombre, precio_base, stock_cantidad,  habilitado, categoria)
            self._componentes = list(componentes)
            if(descuento < 0 or descuento >= 1):
                raise ValueError("El descuento debe ser un numero decimal entre 0 y 1")
            self._descuento = descuento
    
    @property
    def componentes(self) ->tuple[Producto]:
        return tuple(self._componentes)

    def precio_final(self, cantidad: float) -> float:
        cantidad = float(cantidad)
        if (not (cantidad).is_integer() or cantidad < 1):
            raise ValueError("La cantidad debe ser un numero entero mayor que 0")
        
        return self.precio_base  * (1 - self._descuento) * cantidad 
    
class ProductoDestacado():
    def __init__(self, destacado : Producto, orden : int):
        self._producto = destacado
        self._orden_vidriera =  orden

    @property
    def producto(self):
        return self._producto
    @property
    def orden_vidriera(self):
        return self._orden_vidriera

class Exportable(Protocol):
    def exportar(self) -> str:
        ...
        

def exportar_catalogo(items: list[Exportable]) -> list[str]:
    exportacion = list()
    for item in items:
        exportacion.append(item.exportar())
    return exportacion

