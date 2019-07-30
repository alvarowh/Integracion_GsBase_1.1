
import json
from woocommerce import API
import os
import datetime
import sys
import re
import collections
from urllib.parse import urlparse

# SWITCHER para pasar categorias de GsBase a WC.
def hombre():
    return 21


def camisa():
    return 22

def toWCcategory(argument):
    switcher = {
        "01": hombre(),
        "0104": camisa()
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument)
    # Execute the function
    return func

def getCategories(my_product):

    categories= [
        {
            "id": toWCcategory(my_product["general"]["grupo"])
        },
        {
            "id": toWCcategory(my_product["general"]["subgrupo"])
        }
        ]
    return categories


#SWITCHER para pasar colores de GsBase a WC.


def blanco1():
    return "Blanco"


def azul1():
    return "Azul"

def azul2():
    return "Azul Oscuro"

def azul6():
    return "Azul Electrico"

def rojo1():
    return "Rojo"

def verde1():
    return "Verde"

def negro1():
    return "Negro"

def gris1():
    return "Gris"

def rojo2():
    return "Burdeos"

def rojo6():
    return "Rojo Fuego"
#Crear en WooCommerce
def variado19():
    return "Variado"

def vaquero1():
    return ("Vaquero")

def toWCcolor(argument):

    switcher = {
        "010": blanco1(),
        "030": azul1(),
        "031": azul2(),
        "071": rojo2(),
        "070": rojo1(),
        "090": verde1(),
        "020": negro1(),
        "021": gris1(),
        "075": rojo6(),
        "035": azul6(),
        "150": vaquero1(),
        "856": variado19()
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument)
    # Execute the function
    return func

def toWCcolorList(colores):
    nombrecolores=[]
    for color in colores:
        nombrecolores.append(toWCcolor(color))
    return nombrecolores

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
        print("Secret Keys File not available")
        print(e)
        sys.exit()

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
    try:
        if my_json['images']:

            for image in my_json['images']:
                my_image_array.append([image['id']])


    except KeyError as e:
        print(e)

    return my_image_array


def getColorsAndSizes(my_product, numero_almacen):

    resumen_cantidades = []
    colores = []
    tallas = []


    for color in my_product["stock"][numero_almacen]:
        cantidades = {}
        colores.append(color)

        for talla in my_product["stock"][numero_almacen][color]:
            if talla not in tallas:
                tallas.append(talla)

            cantidad=(my_product["stock"][numero_almacen][color][talla])
            pair = {talla: cantidad}
            cantidades.update(pair)

        resumen_cantidades.append(cantidades)
    return resumen_cantidades,colores,tallas


def basicProductJsonCheck(my_product):

    if (my_product["general"]["codigo"]) and (my_product["general"]["denominacion_articulo"]):
        if (my_product["general"]["grupo"]) and (my_product["general"]["subgrupo"]):
            if (my_product["stock"]):
                return True
    else:
        return False

def generateImageResources(global_sku,colores,imagenes_src,images_dict):

    #Defino recursos de imagenes como  y como diccionario
    image_resources = []
    product_image_dict = collections.defaultdict(list)

    print("Imagenes disponibles para "+global_sku)
    #Extraigo las imagenes disponibles para este producto del diccionario globad de imagenes "Images_dict"
    imagenes_producto=(images_dict[global_sku])

    #Para cada imagen disponible para mi producto extraigo el color.
    for imagen in imagenes_producto:
        color_foto = re.findall('(?<=\_)(.*?)(?=\_)', imagen)[0]

        #Compruebo si el color de la foto esta entre los colores de los productos a crear.
        for i,color in enumerate(colores):
            if color_foto==color:

                #Si es asi lo agrego al diccionario de imagenes del producto en concreto "product_image_dict"
                product_image_dict[color].append(imagen)

    #Tambien añado las imagenes a "images_resources" como lista.
    for color in colores:
        for image in product_image_dict[color]:
            src_image={"src": imagenes_src +image }
            image_resources.append(src_image)
    print(image_resources)
    return image_resources, product_image_dict

def getAvailableImages(global_sku,images_src):

    available_images=[]

    return available_images

def checkProductCreation(my_json):
    try:
        if my_json["id"]:
            return True
    except KeyError:
        try:
            if my_json["code"] == 'product_invalid_sku':
                print("El producto ya existe, ID: "+str(my_json["data"]["resource_id"]))
            else:
                if my_json["code"] == 'woocommerce_product_image_upload_error':
                    print("Error Carga de Imagenes: \n" + my_json["message"])
        except Exception as e:
            print("Se ha producido un fallo no contemplado")
            print(e)
            return False
        return False

def basicCreationReport(failed_attemps,succesful_attemps,images=True):


    if images:
        print("\nINFORME DE CREACION DE PRODUCTOS\n")
    else:
        print("\nINFORME DE CREACION DE PRODUCTOS SIN IMÁGENES \n")
    print("CON EXITO " + str(len(succesful_attemps))+"\n")
    for k in succesful_attemps:
        print(k, succesful_attemps[k])

    print("\n\n")
    print("CON FALLOS "+str(len(failed_attemps))+"\n")
    for k in failed_attemps:
        print(k, failed_attemps[k])


def productSplitJSON(directorio_input_json,directorio_output_json):

    product_SKU_list=[]
    # Leo los JSON de GsBase del directorio input json
    included_extensions = ['json']
    file_names = [fn for fn in os.listdir(directorio_input_json)
                  if any(fn.endswith(ext) for ext in included_extensions)]

    for file in file_names:
        if file.startswith("Articulos"):
            print("\n")
            print("----------------------------------------------------------------")
            print("Abriendo fichero: " + file)
            try:
                with open(directorio_input_json + file, 'r') as f:
                    my_big_products = json.loads(f.read())
                    for k in my_big_products:
                        product_SKU_list.append(k)
            except json.decoder.JSONDecodeError as error:
                print(error)
                print("No fue posible abrir el archivo: " + file)
                print("\n")
                continue

    for product in product_SKU_list:
        print(my_big_products[product]["General"]["Codigo"])
        print("General")
        print(my_big_products[product]["General"])
        print("Precios Detallados")
        print(my_big_products[product]["Precios_Detallados"])
        print("Stock")
        print(my_big_products[product]["Stock"])
        print("\n")
        print("----------------------------------------------------------------")