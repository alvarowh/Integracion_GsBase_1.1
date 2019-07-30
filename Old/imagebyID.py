# Busca un producto padre por SKU y devuelve el ID y el SKU de sus hijos (variaciones)

# Si no hay conexion.
# Manera de no tener que extraer todos los productos

from woocommerce import API
import json
import wc_gsbase_api

imagenes_src ="https://camanwi.com/imagesResources/"
data= imagenes_src + "105986_010_1.png"

def searchImageID():

    # Obtengo las claves
    api_keys = wc_gsbase_api.getApiKeys("secret_keys.json")

    # Crea conexion API con WooCommerce

    wpapi= wc_gsbase_api.getApiParametersWP(api_keys)
    # Consigue lista de todos los productos (puede que sean solo los 10 ultimos por la pagination)

    my_json=(wpapi.get("media").json())
    print(json.dumps(my_json, indent=4, sort_keys=True))


#searchImageID()
def postImageandRetrieveID():

    # Obtengo las claves
    api_keys = wc_gsbase_api.getApiKeys("secret_keys.json")

    # Crea conexion API con WooCommerce

    wpapi= wc_gsbase_api.getApiParametersWP(api_keys)
    # Consigue lista de todos los productos (puede que sean solo los 10 ultimos por la pagination)

    data = {

        "src": imagenes_src +"105986" + "_010_1.png",

    }
    my_json=(wpapi.post("media",data).json())
    print(json.dumps(my_json, indent=4, sort_keys=True))


postImageandRetrieveID()