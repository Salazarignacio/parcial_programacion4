from abc import ABC, abstractmethod
from enum import Enum

class UnidadMedida(Enum):
    KILOGRAMO = "kg"
    LITRO = "l"
    UNIDAD = "u"

class ProductoCategoria(Enum):
    ALIMENTOS = "Alimentos"
    BEBIDAS = "Bebidas"
    ELECTRONICA = "Electrónica"
    ROPA = "Ropa"
    HOGAR = "Hogar"

class Categoria:
    def __init__(self, nombre: str):
        self.nombre = nombre

class  Producto(ABC):
    def __init__(self, nombre: str, precio_base: float, stock_cantidad: float, unidad_venta: UnidadMedida):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = nombre
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")
        self._precio_base = precio_base
        if stock_cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")
        self._stock_cantidad = stock_cantidad
        self._unidad_venta = UnidadMedida | None = None
        self._habilitado = True
        self._clasificaciones : list[ProductoCategoria] = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def unidad_venta(self):
        return self._unidad_venta

    @property
    def disponible(self):
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self, cantidad: float): str
        if self.unidad_venta:
            return f"{self.precio_base:.2f} {self.unidad_venta.value}"
        return f"{self.precio_base:.2f}"

    @abstractmethod
    def precio_final(self, cantidad: float): float

    def habilitar(self): None
        
    def deshabilitar(self): None

    def clasificar_en(categoria: Categoria, es_principal: bool): None

    def categorias(self): tuple[ProductoCategoria]: None

    def categoria_principal(self): Categoria

    def exportar(): str

