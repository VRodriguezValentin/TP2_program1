import PAQUETE_PRODUCTOS.archivos as arch

class Paquete:
    def __init__(self, codigo, detalle, usd_compra, usd_venta, peso):
        self.codigo = codigo
        self.detalle = detalle
        self.usd_compra = usd_compra
        self.usd_venta = usd_venta
        self.peso = peso


    def producto_alta(path: str, inv1: list, inv2: list = [0]) -> bool:
        arch.escribir_csv(path, inv1)
        return True

    def producto_baja(path: str):#, inv1: list, inv2: list = [0]) -> bool:
        return arch.leer_csv(path)
    
    def producto_modificar_compra(path: str, codigo: str, lista: list, usd_compra: int = None):
        if usd_compra != None:
                    for producto in lista:
                        if codigo in producto:
                            producto[1] = usd_compra
                            return 'Producto modificado con exito!'
        return 'No se realizaron modificaciones'

    def producto_modificar_venta(path: str, codigo: str, lista: list, usd_venta: int = None):
        if usd_venta != None:
                    for producto in lista:
                        if codigo in producto:
                            producto[2] = usd_venta
                            return 'Producto modificado con exito!'
        return 'No se realizaron modificaciones'

    def producto_listar(path: str, inv1: list, inv2: list = [0]):
        lista_productos = []
        for producto in  inv1:
            lista_productos.append(producto)
        return lista_productos

