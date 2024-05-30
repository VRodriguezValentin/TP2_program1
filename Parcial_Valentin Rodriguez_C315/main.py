import os
import re
import PAQUETE_PRODUCTOS.procesos as ps
import PAQUETE_PRODUCTOS.menu as m
import PAQUETE_PRODUCTOS.paquetes as pq
import PAQUETE_PRODUCTOS.depositos as depo




def validar_codigo(codigo):
    patron = r'^\d{4}-[a-zA-Z]{2}$'
    if re.match(patron, codigo):
        return True
    else:
        return False
    
def validar_peso(peso):
    patron = r'^\d+\s?(g|gr)$'
    if re.match(patron, peso):
        return True
    else:
        return False
def validar_cuil(cuil):
    patron = r'^\d{2}-\d{8}-\d$'
    if re.match(patron, cuil):
        return True
    else:
        return False


def main():
    #Inicializacion de variables
    opciones = ['0','1','2','3','4','5','6','7','8','9','10']
    opciones_menu = ['Alta de Producto', 'Baja de Producto', 'Modificacion de Producto', 'Listado de Productos', 'Importar Producto', 'Vender Producto', 'Listar Estado de Depositos','Bucar Producto con Menos Stock','Filtrar Productos por Precio de Media','Ordenar Depositos por Peso']
    vector_total_productos = pq.Paquete.productos_listar_cantidad('DB_PRODUCTOS.csv')
    vector_codigos = pq.Paquete.productos_listar('DB_PRODUCTOS.csv')
    lista_aux = []

    while True:
        opcion = m.menu('MENU PRODUCTOS',opciones_menu)
        opcion = ps.validacion_lista(opcion, opciones, 'opcion')
        os.system('cls')

        if opcion == '0':
            print('¡Hasta luego!')
            break
        else:
            match opcion:
                case '1':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t\t   Alta de Producto\n╚══════════════════════════════════════════════════╝\n')
                    while True:
                        codigo = input('Formato: [NNNN-XX]\nIngrese un codigo: ')
                        codigo_valido = validar_codigo(codigo)
                        if codigo_valido == False:
                            os.system('cls')
                            print('¡ERROR! El codigo no es valido\n')
                            break
                        else:
                            existe_codigo = False
                            for producto in vector_codigos:
                                if codigo in producto:
                                    print('[ERROR] Ítem existente.')
                                    existe_codigo = True
                                    break
                            if existe_codigo:
                                break
                            else:
                                while True:
                                    os.system('cls')
                                    detalle = ps.get_str('Ingrese el nombre del producto: ', '¡ERROR! El nombre del producto no es valido', 25)
                                    if len(detalle) > 0:
                                        break
                                os.system('cls')
                                usd_compra = ps.get_int('Ingrese un valor de importacion: ','¡ERROR! El valor de importacion no es valido', 0)
                                os.system('cls')
                                usd_venta = ps.get_int('Ingrese un valor de comercializacion: ','¡ERROR! El valor de comercializacion no es valido', 0)
                                os.system('cls')
                                cantidad_productos = ps.get_int('Ingrese la cantidad de productos: ','¡ERROR! La cantidad de productos no es valida', 0)
                                os.system('cls')
                                while True:
                                    peso = input('Formato: [(num)gr | (num)g]\nIngrese un peso: ')
                                    peso_valido = validar_peso(peso)
                                    if peso_valido == False:
                                        os.system('cls')
                                        print('¡ERROR! El peso no es valido\n')
                                    else:
                                        break
                                os.system('cls')
                                vector_codigos.append([codigo, detalle, usd_compra, usd_venta, peso, cantidad_productos])
                                vector_total_productos.append((codigo, cantidad_productos))

                                lista_aux = vector_codigos.copy()
                                nuevo_producto = lista_aux.pop()
                                print(f'aux: {lista_aux}')
                                print('\n')
                                print(f'aux: {vector_codigos}')
                                pq.Paquete.producto_alta('DB_PRODUCTOS.csv',nuevo_producto)
                                depo.Gestion.log(f'Alta de producto. PRODUCTO {codigo}')
                                for producto in vector_codigos:
                                    if codigo in producto:
                                        print(f'Producto: {producto}')
                                        break
                                for total in vector_total_productos:
                                    if codigo in total:
                                        print(f'Total de productos: {total}')
                                break
                case '2':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t    Baja de Producto\n╚══════════════════════════════════════════════════╝\n')
                    while True:
                        retorno = pq.Paquete.productos_listar('DB_PRODUCTOS.csv')
                        for productos in retorno:
                            print(f'{productos}\n')
                        codigo_aux = input('Formato: [NNNN-XX]\nIngrese un codigo: ')
                        codigo_valido = validar_codigo(codigo_aux)
                        if codigo_valido == False: 
                            os.system('cls')
                            print('¡ERROR! El codigo no es valido\n')
                            break
                        else:
                            existe_codigo = False
                            for producto in vector_codigos:
                                if codigo_aux in producto:
                                    existe_codigo = True
                                    break
                            if existe_codigo == False:
                                print('[ERROR] Ítem no existente.')
                                break
                            else:
                                continuar = False
                                for cant in vector_total_productos:
                                        if codigo_aux in cant:
                                            if cant[1] == '0' or cant[1] == 0:
                                                continuar = True
                                                vector_codigos.remove(producto)
                                                vector_total_productos.remove(cant)
                                                break
                                if continuar:
                                    retorno = pq.Paquete.producto_baja('DB_PRODUCTOS.csv', vector_codigos)
                                    if retorno:
                                        os.system('cls')
                                        print(f'Producto: {producto}\nProducto dado de baja')
                                    break
                                else:
                                    print('[ERROR] Ítem con stock')
                                    break

                case '3':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n Modificación de Producto\n╚═════════════════════════════════════════════════════╝\n')
                    while True:
                        retorno = pq.Paquete.productos_listar('DB_PRODUCTOS.csv')
                        for productos in retorno:
                            print(f'{productos}\n')
                        codigo_aux = input('Formato: [NNNN-XX]\nIngrese un codigo: ')
                        codigo_valido = validar_codigo(codigo_aux)
                        if codigo_valido == False:
                            os.system('cls')
                            print('¡ERROR! El codigo no es valido\n')
                            break
                        else:
                            existe_codigo = False
                            for producto in vector_codigos:
                                if codigo_aux in producto:
                                    existe_codigo = True
                                    break
                            if existe_codigo == False:
                                print('[ERROR] Ítem no existente.')
                                break
                            else:
                                cambiar_usd_compra = ps.validacion_continuar('¿Desea modificar el valor de importacion?\n => ')
                                if cambiar_usd_compra:
                                    usd_compra_mod = ps.get_int('Ingrese un valor de importacion: ','¡ERROR! El valor de importacion no es valido', 0)
                                    for producto in vector_codigos:
                                        if codigo_aux in producto:
                                            producto[2] = usd_compra_mod
                                            print(f'Producto actualizado: {producto}')
                                    rtn1 = pq.Paquete.producto_modificar_compra('DB_PRODUCTOS.csv', codigo_aux, vector_codigos, usd_compra_mod)
                                    print(rtn1)
                                
                                cambiar_usd_venta = ps.validacion_continuar('¿Desea modificar el valor de comercializacion?\n => ')
                                if cambiar_usd_venta:
                                    usd_venta_mod = ps.get_int('Ingrese un valor de comercializacion: ','¡ERROR! El valor de comercializacion no es valido', 0)
                                    for producto in vector_codigos:
                                        if codigo_aux in producto:
                                            producto[3] = usd_venta_mod
                                            print(f'Producto actualizado: {producto}')
                                    rtn2 = pq.Paquete.producto_modificar_venta('DB_PRODUCTOS.csv', codigo_aux, vector_codigos, usd_venta_mod)
                                    print(rtn2)
                                break
                case '4':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t Listado de Productos\n╚═════════════════════════════════════════════════════╝\n')
                    retorno = pq.Paquete.productos_listar('DB_PRODUCTOS.csv')
                    for productos in retorno:
                        print(f'{productos}\n')
                    #print(f'Productos:\n{retorno}')
                case '5':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t Importar Producto\n╚═════════════════════════════════════════════════════╝\n')
                    while True:
                        retorno = pq.Paquete.productos_listar('DB_PRODUCTOS.csv')
                        for productos in retorno:
                            print(f'{productos}\n') 
                        codigo_aux = input('Formato: [NNNN-XX]\nIngrese un codigo: ')
                        codigo_valido = validar_codigo(codigo_aux)
                        if codigo_valido == False:
                            os.system('cls')
                            print('¡ERROR! El codigo no es valido\n')
                            break
                        else:
                            existe_codigo = False
                            for producto in vector_codigos:
                                if codigo_aux in producto:
                                    existe_codigo = True
                                    break
                            if existe_codigo == False:
                                print('[ERROR] Ítem no existente.')
                                break
                            else:
                                for cant in vector_total_productos:
                                    if codigo_aux in cant:
                                        cantidad = int(cant[1])
                                        print(f'Cantidad: {cantidad}')
                                        depo.Gestion.importar('DB_PRODUCTOS.csv', 'DEPOSITOS.json', codigo_aux, cantidad)
                                        break
                        break
                case '6':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t Vender Producto\n╚═════════════════════════════════════════════════════╝\n')
                    while True:
                        retorno = pq.Paquete.productos_listar('DB_PRODUCTOS.csv')
                        for productos in retorno:
                            print(f'{productos}\n')
                        codigo_aux = input('Formato: [NNNN-XX]\nIngrese un codigo: ')
                        codigo_valido = validar_codigo(codigo_aux)
                        if codigo_valido == False:
                            os.system('cls')
                            print('¡ERROR! El codigo no es valido\n')
                        else:
                            existe_codigo = False
                            for producto in vector_codigos:
                                if codigo_aux in producto:
                                    existe_codigo = True
                                    break
                            if existe_codigo == False:
                                print('[ERROR] Ítem no existente.')
                                break
                            else:
                                for cant in vector_total_productos:
                                    if codigo_aux in cant:
                                        cantidad = int(cant[1])
                                        print(f'Cantidad: {cantidad}')
                                        cantidad_seleccionar = ps.get_int('Ingrese la cantidad: ','¡ERROR! La cantidad no es valida', 0, cantidad)
                                        break
                        
                                cuil = input('Formato: [NN-NNNNNNNN-N]Ingrese el CUIL del comprador: ')
                                cuil_valido = validar_cuil(cuil)
                                if cuil_valido == False:
                                    print('[ERROR] El CUIL no es valido')
                                    break
                                else:
                                    cotizacion_usd = ps.get_int('Ingrese un valor de cotizacion: ','¡ERROR! El valor de cotizacion no es valido', 1) 
                                    depo.Gestion.vender('DEPOSITOS.json', 'DB_PRODUCTOS.csv', codigo_aux, cantidad_seleccionar, cuil, cotizacion_usd)
                                    break
                case '7':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t Listar Estado de Depositos\n╚═════════════════════════════════════════════════════╝\n')
                    depositos = depo.Gestion.cargar_depositos('DEPOSITOS.json')
                    for deposito in depositos:
                        capacidad_dispo = depo.Deposito.__len__(deposito)
                        capacidad_max = deposito.capacidad
                        ocupado = capacidad_max - capacidad_dispo
                        print(f'ID {deposito.id} - {ocupado}/{capacidad_max} - Disponible {capacidad_dispo}')
                case _:
                    print('¡ERROR! La opcion no es valida')
        
        input('Presione ENTER para continuar...')
        os.system('cls')

main()