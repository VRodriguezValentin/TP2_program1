from datetime import datetime
import PAQUETE_PRODUCTOS.archivos as arch

class Deposito:
    def __init__(self, capacidad = 1000):
        _id_deposito = 1
        self.id = _id_deposito
        _id_deposito += 1
        self.capacidad = capacidad
        self.stock = []
        
    def __len__(self):
        ocupado = 0
        for item in self.stock:
            ocupado += item['cantidad']
        return self.capacidad - ocupado

    def introducir_producto(self, codigo, cantidad):
        if len(self) < cantidad:
            return 'El deposito no tiene suficiente capacidad disponible.'
        
        for producto in self.stock:
            if producto['item'] == codigo:
                producto['cantidad'] += cantidad
                return 'Producto sumado al deposito.'
        
        self.stock.append({'item': codigo, 'cantidad': cantidad})
        return 'Producto agregado al deposito.'
    
    def retirar_producto(self, codigo, cantidad):
        for producto in self['stock']:
            if producto['item'] == codigo:
                if producto['cantidad'] < cantidad:
                    return 'No hay suficiente stock para retirar.'
                
                producto['cantidad'] -= cantidad
                if producto['cantidad'] == 0:
                    self['stock'].remove(producto)
                return 'Producto retirado del deposito'
        return 'El producto no se encuentra en el deposito.'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Gestion:
    def importar(path, depositos_path, codigo, cantidad):
        cantidad_restante = cantidad
        depositos_data = arch.leer_json(depositos_path)
        depositos = []

        for depo in depositos_data:
            deposito = Deposito(depo['capacidad'])
            deposito.id = depo['id']
            deposito.stock = depo['stock']
            depositos.append(deposito)

        for deposito in depositos:
            capacidad_disponible = len(deposito)
            if capacidad_disponible > 0:
                if cantidad_restante <= capacidad_disponible:
                    deposito.introducir_producto(codigo, cantidad_restante)
                    cantidad_restante = 0
                else:
                    deposito.introducir_producto(codigo, capacidad_disponible)
                    cantidad_restante -= capacidad_disponible

                if cantidad_restante == 0:
                    break

        while cantidad_restante > 0:
            nuevo_deposito = Deposito()
            capacidad_disponible = len(nuevo_deposito)
            if cantidad_restante <= capacidad_disponible:
                nuevo_deposito.introducir_producto(codigo, cantidad_restante)
                cantidad_restante = 0
            else:
                nuevo_deposito.introducir_producto(codigo, capacidad_disponible)
                cantidad_restante -= capacidad_disponible
            depositos.append(nuevo_deposito)

        Gestion.guardar_depositos(depositos, depositos_path)
        Gestion.log(f'Importacion exitosa! PRODUCTO {codigo} - CANTIDAD {cantidad}')

    def vender(depositos_path, path, codigo, cantidad, cuit_comprador, cotizacion_usd):
        base_datos_productos = arch.leer_csv(path)
        for producto in base_datos_productos:
            if producto[0] == codigo:
                cantidad_total = int(producto[5])
                if cantidad_total < cantidad:
                    return('No hay suficiente stock en el inventario')
                cantidad_total -= cantidad
                break
        else:
            return('El producto no se encuentra en el inventario')

        cantidad_restante = cantidad
        depositos = arch.leer_json(depositos_path)
        for deposito in depositos:
            for item in deposito['stock']:
                if item['item'] == codigo:
                    if item['cantidad'] >= cantidad_restante:
                        print(Deposito.retirar_producto(deposito,codigo, cantidad_restante))
                        cantidad_restante = 0
                    else:
                        cantidad_restante -= item['cantidad']
                        print(Deposito.retirar_producto(deposito,codigo, item['cantidad']))

                    if cantidad_restante == 0:
                        break
            if cantidad_restante == 0:
                break

        depositos = list(filter(lambda depo: len(depo['stock']) > 0, depositos))
        Gestion.guardar_depositos(depositos, depositos_path, 'd')

        cotiza = int(cotizacion_usd) 
        valor_usd = int(producto[3])
        importe_usd = valor_usd * cantidad
        importe_ars = importe_usd * cotiza
        Gestion.generar_ticket(cuit_comprador, codigo, cantidad, importe_usd, importe_ars, cotiza)
        Gestion.log(f'Venta exitosa! PRODUCTO {codigo} - COMPRADOR {cuit_comprador} - IMPORTE {importe_ars}')
        return 'Venta realizada con exito'

    def generar_ticket(cuit_comprador, codigo, cantidad, importe_usd, importe_ars, cotizacion_usd):
        fecha_hora_actual = datetime.now()
        formato = fecha_hora_actual.strftime('%d/%m/%Y %H:%M')
        ticket = (f'[VENTA {formato}]\nCUIT COMPRADOR: {cuit_comprador}\nDETALLE PRODUCTO: {codigo}\nCANTIDAD VENDIDA: {cantidad}\nIMPORTE USD: {importe_usd}\nIMPORTE ARS: {importe_ars}\nCOTIZACION DEL DIA: {cotizacion_usd}\n')

        arch.escribir_txt('ventas.txt',ticket,'a')
        print(ticket)
    
    def guardar_depositos(depositos, depositos_path, tipo: str = 'o'):
        if tipo == 'd':
            depositos_data = []
            for deposito in depositos:
                depo = {'id': deposito['id'], 'capacidad': deposito['capacidad'], 'stock': deposito['stock']}
                depositos_data.append(depo)
        else:
            depositos_data = []
            for deposito in depositos:
                depo = {'id': deposito.id, 'capacidad': deposito.capacidad, 'stock': deposito.stock}
                depositos_data.append(depo)
        arch.escribir_json(depositos_path,depositos_data)

    def cargar_depositos(depositos_path):
        depositos_data = arch.leer_json(depositos_path)
        depositos = []
        for data in depositos_data:
            deposito = Deposito(data['capacidad'])
            deposito.id = data['id']
            deposito.stock = data['stock']
            depositos.append(deposito)
        return depositos

    def log(mensaje):
        fecha_hora_actual = datetime.now()
        formato = fecha_hora_actual.strftime('%d/%m/%Y %H:%M')
        data = f'{formato} : {mensaje}'
        arch.escribir_txt('log.txt',data,'a')