#UPDATES PRODUCTS BY BY ONE FROM DIFFERENT JSON FILES


from woocommerce import API
import json
import time
import wc_gsbase_api
import os

start=time.time()

# Parametros de Importacion.
numero_almacen = "99"
directorio_input_json = "C:/Users/alvar/Documents/ferrer/Interactivo_16_07/update/"


# Obtengo credenciales API.

api_keys = wc_gsbase_api.getApiKeys('../../secret_keys.json')


# Crea conexion API con WooCommerce
wcapi = wc_gsbase_api.getApiParameters(api_keys)

#Obtengo lista de productos

my_products_json = wc_gsbase_api.getProductList(wcapi, 50)

# Leo los JSON de GsBase con los datos de los productos a actualizar

for test_filename in os.listdir(directorio_input_json):

    with open(directorio_input_json+test_filename, 'r') as f:
        my_template = json.loads(f.read())


    # Extraigo stock detallado por tallas y colores para cada producto
    colores = []
    tallas = []
    resumen_cantidades = []
    nombrecolores=[]

    resumen_cantidades,colores,tallas,nombrecolores = wc_gsbase_api.getColorsAndSizes(my_template,numero_almacen)

    #Extraigo categorias de gs base y transformo a WC

    categories = [
                {
                    "id": wc_gsbase_api.toWCcategory(my_template["general"]["grupo"])
                },
                {
                    "id": wc_gsbase_api.toWCcategory(my_template["general"]["subgrupo"])
                }
            ]


    # Busco el producto padre para cada color y extraigo las variaciones.

    global_sku = my_template["general"]["codigo"]
    retrievedIDs = (wc_gsbase_api.getChildIDsFromParentSKU(str(global_sku), my_products_json))
    parent_id = retrievedIDs[0]
    child_id = retrievedIDs[1]
    child_id.sort()


    if parent_id != "0":

        my_variations=[]
        i=0
        for e, color in enumerate(colores,0):

            # Cada talla y color es una variante con su propio Id.
            for d, talla in enumerate(tallas, 0):

                variation = {
                    "id": child_id[i],
                    "stock_quantity": resumen_cantidades[e][talla],
                    "regular_price": my_template["general"]["pvp"]
                }
                my_variations.append(variation)
                i += 1
            #Creo el diccionario data que contiene los datos a enviar a WC a través de la api para cada producto padre.
        data = {

            "update": my_variations
        }
        #Envio la actualizacion a WC.
        print("Enviando datos de s variantes ID:"+str(parent_id)+ "con SKU:" +global_sku)
        start2 = time.time()
        my_json = (wcapi.put("products/"+str(parent_id)+"/variations/batch", data).json())
        print("Stock actualizado a: " + str(resumen_cantidades))
        end2 = time.time()
        print("Actualizar este producto ha tomado "+("{0:.2f}".format(end2-start2))+" segundos.")
        print("\n")

    else:
        print("Cannot find ID for SKU:"+global_sku)

end = time.time()

print("La actualizacion completa ha tomado "+("{0:.2f}".format(end-start))+" segundos.")