import json
import datetime
import os
import wc_gsbase_api

def getOldOrders(wcapi):

    old_orders = {}

    # Obtengo los pedidos de WooCommmerce
    try:
        my_json = (wcapi.get("orders").json())
    except ConnectionError as e:
        print(e)
        print("Cannot retrieve old orders")
    else:
        # Guardo Numero de pedido y Fecha en diccionario old_orders.
        for attribute in my_json:
            old_orders.update({attribute['id']: attribute['date_created_gmt']})

    return old_orders

def getNewOrders(old_orders,wcapi):

    new_orders = {}
    resultado=""

    # Conecto para buscar nuevas ordenes.
    try:
        my_json = (wcapi.get("orders").json())
    except Exception as e:
        print("type error: " + str(e))
        print("Cannot retrieve new orders")
    else:
        for attribute in my_json:
            new_orders.update({attribute['id']: attribute['date_created_gmt']})


        # Compruebo que existen ordenes y obtengo la ultima clave de cada diccionario
        if len(new_orders) > 0 and len(old_orders) > 0:
            oofk = next(iter(old_orders))
            nofk = next(iter(new_orders))

            # Acciones si hay nuevas ordenes.
            if oofk != nofk and nofk > oofk:
                print('Hay nuevos pedidos')

                # Imprimo por pantalla las nuevas ordenes.
                orders = (dict(new_orders.items() - old_orders.items()))
                print(orders)
                old_orders.clear()
                old_orders.update(new_orders)

                # Paso los detalles de las nuevas ordenes a un JSON.
                new_orders_json = []
                for i in range(len(orders)):
                    new_orders_json.append(my_json[i])

                # Guardo un archivo JSON con la fecha actual que contiene las ordenes nuevas.

                #Path Name
                pathname = wc_gsbase_api.getOrderPath()

                #File Name
                filename = wc_gsbase_api.getFileName(new_orders_json)

                with open(pathname+filename, 'w') as json_file:
                    json.dump(new_orders_json, json_file)

                resultado = orders
                print(resultado)
            # Acciones si no hay nuevas ordenes.
            else:
                resultado = datetime.datetime.now().strftime("%mm/%dd %Hh:%Mm")+" No hay nuevos pedidos \n"
                print(resultado)

        else: resultado = datetime.datetime.now().strftime("%mm/%dd %Hh:%Mm")+" No hay nuevos pedidos \n"

    return resultado






