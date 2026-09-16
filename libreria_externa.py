# libreria_externa .py — SE ENTREGA. NO SE MODIFICA.
class FichaPuntoDeVenta:
    def __init__(self, codigo: str, detalle: str) -> None:
        self._codigo = codigo
        self._detalle = detalle
    def exportar(self) -> str:
        return f"POS|{self._codigo}|{self._detalle}"
"""Ficha que genera el sistema de caja de un tercero."""