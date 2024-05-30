import PAQUETE_PRODUCTOS.archivos as arch

class Paquete:
    def __init__(self, codigo, detalle, usd_compra, usd_venta, peso):
        self.codigo = codigo
        self.detalle = detalle
        self.usd_compra = usd_compra
        self.usd_venta = usd_venta
        self.peso = peso


    def productos_listar(path: str) -> list:
        lista_productos = []
        leer = arch.leer_csv(path)
        for linea in leer:
            lista_productos.append(linea)
        return lista_productos

    def productos_listar_cantidad(path: str) -> list:
        lista_productos = []
        leer = arch.leer_csv(path)
        for linea in leer:
            pos_cantidad = linea[0],linea[5]
            lista_productos.append(pos_cantidad)
        return lista_productos

    def producto_alta(path: str, producto: list, cantidad: list = 0) -> bool:
        arch.escribir_csv(path,producto,'a')
        return True

    def producto_baja(path: str, lista: list) -> bool:
        arch.escribir_csv_mas(path, lista)
        return True

    
    def producto_modificar_compra(path: str, codigo: str, lista: list, usd_compra: int = None):
        if usd_compra != None:
            for producto in lista:
                if codigo in producto:
                    producto[2] = usd_compra
            arch.escribir_csv_mas(path,lista)
            return 'Producto modificado con exito!'
        else:
            return 'No se realizaron modificaciones'

    def producto_modificar_venta(path: str, codigo: str, lista: list, usd_venta: int = None):
        if usd_venta != None:
            for producto in lista:
                if codigo in producto:
                    producto[3] = usd_venta
            arch.escribir_csv_mas(path,lista)
            return 'Producto modificado con exito!'
        else:
            return 'No se realizaron modificaciones'