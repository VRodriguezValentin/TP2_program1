import os
import re
import PAQUETE_PRODUCTOS.procesos as ps
import PAQUETE_PRODUCTOS.menu as m
import PAQUETE_PRODUCTOS.paquetes as pq



def validar_codigo(codigo):
    patron = r"^\d{4}-[a-zA-Z]{2}$"
    if re.match(patron, codigo):
        return True
    else:
        return False
    
def validar_peso(peso):
    patron = r"^\d+\s?(g|gr)$"
    if re.match(patron, peso):
        return True
    else:
        return False

def main():
    #Inicializacion de variables
    opciones = ['0','1','2','3','4']#...
    opciones_menu = ['Alta de Producto', 'Baja de Producto', 'Modificacion de Producto', 'Listado de Productos']#...
    vector_codigos = list()
    vector_total_productos = [0]

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
                        else:
                            existe_codigo = False
                            for producto in vector_codigos:
                                if codigo in producto:
                                    print('[ERROR] Ítem existente.')
                                    existe_codigo = True
                            if existe_codigo == False:
                                break
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
                    while True:
                        peso = input('Formato: [(num)gr | (num)g]\nIngrese un peso: ')
                        peso_valido = validar_peso(peso)
                        if peso_valido == False:
                            os.system('cls')
                            print('¡ERROR! El peso no es valido\n')
                        else:
                            break
                    os.system('cls')
                    vector_codigos.append({codigo: [detalle, usd_compra, usd_venta, peso]})
                    vector_total_productos[0] += 1
                    pq.Paquete.producto_alta('DB_PRODUCTOS.csv',vector_codigos)
                    for producto in vector_codigos:
                        if codigo in producto:
                            print(f'Producto: {producto}')
                            break
                    for total in vector_total_productos:
                        print(f'Total de productos: {total}')
                case '2':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t    Baja de Producto\n╚══════════════════════════════════════════════════╝\n')
                    while True:
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
                                    vector_codigos.remove(producto)
                                    break
                            if existe_codigo == False:
                                print('[ERROR] Ítem no existente.')
                            else:
                                retorno = pq.Paquete.producto_baja('DB_PRODUCTOS.csv') #no funca
                                break
                case '3':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n Modificación de Producto\n╚═════════════════════════════════════════════════════╝\n')
                    while True:
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
                            else:
                                cambiar_usd_compra = ps.validacion_continuar('¿Desea modificar el valor de importacion?\n => ')
                                if cambiar_usd_compra:
                                    usd_compra_mod = ps.get_int('Ingrese un valor de importacion: ','¡ERROR! El valor de importacion no es valido', 0)
                                    rtn1 = pq.Paquete.producto_modificar_compra('DB_PRODUCTOS.csv', codigo_aux, vector_codigos, usd_compra_mod)
                                    print(rtn1)
                                
                                cambiar_usd_venta = ps.validacion_continuar('¿Desea modificar el valor de comercializacion?\n => ')
                                if cambiar_usd_venta:
                                    usd_venta_mod = ps.get_int('Ingrese un valor de comercializacion: ','¡ERROR! El valor de comercializacion no es valido', 0)
                                    rtn2 = pq.Paquete.producto_modificar_venta('DB_PRODUCTOS.csv', codigo_aux, vector_codigos, usd_venta_mod)
                                    print(rtn2)
                                break
                case '4':
                    os.system('cls')
                    print('╔══════════════════════════════════════════════════╗\n\t Listado de Productos\n╚═════════════════════════════════════════════════════╝\n')
                    retorno = pq.Paquete.producto_listar('DB_PRODUCTOS.csv', vector_codigos)
                    print(f'Productos: {retorno}')
                case _:
                    print('¡ERROR! La opcion no es valida')
                    break
        
        input('Presione ENTER para continuar...')
        os.system('cls')

main()