# Connects to WooCommerce and checks for new orders, if there are it saves them to a JSON file.
#Si no hay ordenes.
#Si no hay conexion
#Guardar en carpeta

from woocommerce import API
import json
import datetime, threading

def mybigfunction():
    # Frecuencia de la comprobacion
    x=10


    old_orders={}

    # Obtengo credenciales API.
    secrets_filename = 'secret_keys.json'

    with open(secrets_filename, 'r') as f:
        api_keys = json.loads(f.read())


    # Crea conexion API con WooCommerce

    wcapi = API(
        url="https://camanwi.com", # Your store URL
        consumer_key=api_keys['WOOCOMMERCE_KEY'], # Your consumer key
        consumer_secret=api_keys['WOOCOMMERCE_SECRET'], # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3", # WooCommerce WP REST API version
        timeout=15
    )

    # Obtengo los pedidos de WooCommmerce
    try:
        my_json = (wcapi.get("orders").json())
    except Exception as e:
        print("type error: " + str(e))
        print("Cannot retrieve old orders")

    # Guardo Numero de pedido y Fecha en diccionario old_orders.
    for attribute in my_json:
        old_orders.update({attribute['id']:attribute['date_created_gmt']})


    # Compruebo si hay nuevas ordenes periodicamente.
    def checkneworders():
        new_orders={}

        # Conecto para buscar nuevas ordenes.
        try:
            my_json = (wcapi.get("orders").json())
        except Exception as e:
            print("type error: " + str(e))
            print("Cannot retrieve new orders")
        for attribute in my_json:
            new_orders.update({attribute['id']:attribute['date_created_gmt']})

        # Compruebo que existen ordenes y obtengo la ultima clave de cada diccionario
        if len(new_orders) > 0:
            oofk = next(iter(old_orders))
            nofk = next(iter(new_orders))

            # Acciones si hay nuevas ordenes.
            if oofk != nofk and nofk > oofk:
                print('Hay nuevos pedidos')

                # Imprimo por pantalla las nuevas ordenes.
                orders=(dict(new_orders.items() - old_orders.items()))

                old_orders.clear()
                old_orders.update(new_orders)

                # Paso los detalles de las nuevas ordenes a un JSON.
                new_orders_json=[]
                for i in range(len(orders)):
                    new_orders_json.append(my_json[i])

                # Guardo un archivo JSON con la fecha actual que contiene las ordenes nuevas.
                order_date=(datetime.datetime.now().strftime("%Y%m%d_%H%M"))
                with open('orders_'+order_date+'.json', 'w') as json_file:
                    json.dump(new_orders_json, json_file)
                resultado=orders
                print(resultado)
            # Acciones si no hay nuevas ordenes.
            else:
                resultado="No hay nuevos pedidos"
                print(resultado)

        threading.Timer(x, checkneworders).start()


    checkneworders()
