from abc import ABC, abstractmethod

class UnidadMedida:
    pass

class Categoria:
    def __init__(self, nombre: str, descripcion: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoria no puede esta vacio")
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self):
        return self._nombre
    @property
    def descripcion(self):
        return self._descripcion

class ProductoCategoria():
    def __init__(self, nombre: str, descripcion: str, categoria : Categoria ):
        
        self._categoria = categoria
        self._es_principal = False

    @property
    def es_principal(self):
        return self._es_principal
    @property
    def marcar_principal(self, valor: bool):
        self.es_principal = valor


class Producto(ABC):
    def __init__(self, nombre: str, precio_base: float, stock_cantidad: float,  unidad_venta: UnidadMedida | None = None):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = nombre
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")
        self._precio_base = precio_base
        if stock_cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")
        self._stock_cantidad = stock_cantidad
        self._unidad_venta = unidad_venta
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
    def precio_publicado(self) -> str:
        if self.unidad_venta is not None:
            return f"$ {self.precio_base:.2f} / {self.unidad_venta.simbolo}"
        return f"$ {self.precio_base:.2f}"

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        raise NotImplementedError

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(self, categoria: Categoria, es_principal: bool) -> None:
        self._clasificaciones.append(ProductoCategoria())

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        return None

    def exportar(self) -> str:
        raise NotImplementedError

