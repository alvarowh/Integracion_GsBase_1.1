# SWITCHER para pasar categorias de GsBase a WC.
import json
from woocommerce import API
import os
import datetime

def hombre():
    return 21


def camisa():
    return 22

#group by MIRAR
def toWCcategory(argument):
    switcher = {
        "01": hombre(),
        "0104": camisa()
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument)
    # Execute the function
    return func


#SWITCHER para pasar colores de GsBase a WC.


def blanco1():
    return "Blanco"


def azul1():
    return "Azul"

def azul2():
    return "Azul Oscuro"

def rojo1():
    return "Rojo"

def verde1():
    return "Verde"

def negro1():
    return "Negro"

def gris1():
    return "Gris"

def toWCcolor(argument):

    switcher = {
        "010": blanco1(),
        "030": azul1(),
        "031": azul2(),
        "070": rojo1(),
        "090": verde1(),
        "020": negro1(),
        "021": gris1()
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument)
    # Execute the function
    return func


#CONEXIONA API WC

#Obtengo credenciales API.
def getApiKeys(file):
    secrets_filename = file
    api_keys = {}
    try:

        with open(secrets_filename, 'r') as f:
            api_keys = json.loads(f.read())
        return api_keys

    except IOError as e:
        print("File not available")
        print(e)
        return api_keys


#Defino parametros de conexion
def getApiParameters(api_keys):

    wcapi = API(
        url="https://camanwi.com",  # Your store URL
        consumer_key=api_keys['WOOCOMMERCE_KEY'],  # Your consumer key
        consumer_secret=api_keys['WOOCOMMERCE_SECRET'],  # Your consumer secret
        wp_api=True,  # Enable the WP REST API integration
        version="wc/v3",  # WooCommerce WP REST API version
        timeout=45
    )
    return wcapi

def getApiParametersWP(api_keys):

    wcapi = API(
        url="https://camanwi.com",  # Your store URL
        consumer_key=api_keys['WOOCOMMERCE_KEY'],  # Your consumer key
        consumer_secret=api_keys['WOOCOMMERCE_SECRET'],  # Your consumer secret
        wp_api=True,  # Enable the WP REST API integration
        version="wp/v2",  # WooCommerce WP REST API version
        timeout=15
    )
    return wcapi

#DEVUELVE EL PATH PARA CREAR LOS ARCHIVOS JSON DE ORDENES EN LOCAL

def getOrderPath():

    year = (datetime.datetime.now().strftime("%Y"))
    month = (datetime.datetime.now().strftime("%m"))
    localpath = "C:/Users/alvar/Documents/ferrer/Interactivo_16_07/"
    folderpath = "Orders/" + year + "/" + month + "/"

    pathname = localpath + folderpath

    try:
       os.makedirs(pathname)
    except OSError:
        print("Creation of the directory %s failed" % pathname)
    else:
        print("Successfully created the directory %s" % pathname)

    return pathname

def getFileName(new_orders_json):
    order_id=""

    for order in new_orders_json:
        order_id+=str(order['id'])+"_"

    #order_date = (datetime.datetime.now().strftime("%Yy%mm%dd_%Hh%Mm"))
    filename = str(order_id)+"ID.json"
    return filename



#GETS A LIST OF 50 Products
def getProductList(wcapi, items):

        my_json = (wcapi.get("products?per_page=" + str(items)).json())

        return my_json


#Retrieves child ids from parent SKU
def getChildIDsFromParentSKU(sku, my_json):

    if bool(my_json):

        for attribute in my_json:
            if attribute['sku'] == sku:
                if attribute['variations']:
                    return attribute['id'], attribute['variations']
                else:
                    return "0", "0"
    else:
        return "0", "0"

def getImagesDetails(my_json):

    my_image_array=[]

    if my_json['images']:

        for image in my_json['images']:
            my_image_array.append([image['id']])


    else:
        print ("Product does not contain images")

    return my_image_array


def getColorsAndSizes(my_template, numero_almacen):

    colores = []
    tallas = []
    resumen_cantidades = []
    nombrecolores = []

    for color in my_template["stock"][numero_almacen]:
        cantidades = {}
        colores.append(color)
        nombrecolores.append(toWCcolor(color))
        for talla in my_template["stock"][numero_almacen][color]:
            if talla not in tallas:
                tallas.append(talla)

            cantidad=(my_template["stock"][numero_almacen][color][talla])
            pair = {talla: cantidad}
            cantidades.update(pair)

        resumen_cantidades.append(cantidades)

    return resumen_cantidades,colores,tallas,nombrecolores

def productSplitJSON(directorio_input_json,directorio_output_json):

    # Leo los JSON de GsBase del directorio input json
    included_extensions = ['json']
    file_names = [fn for fn in os.listdir(directorio_input_json)
                  if any(fn.endswith(ext) for ext in included_extensions)]

    for productfile in file_names:
        print(productfile)





