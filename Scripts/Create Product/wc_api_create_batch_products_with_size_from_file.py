#Crea un producto separado por color en WooCommerce desde el JSON de GsBase (SERIE 3). Timeout 30s.

#Comprobar si el producto ya esta creado
#Si falla la creacion del producto padre
#Si no hay conexion
#Mas de 2 fotografias por variacion.



from woocommerce import API
import json
import time
import wc_gsbase_api
import os

# Parametros de Importacion.
numero_almacen = "99"
imagenes_src ="https://camanwi.com/imagesResources/"
directorio_input_json = "C:/Users/alvar/Documents/ferrer/Interactivo_16_07/products/"

# Obtengo credenciales API.
secrets_filename = '../../secret_keys.json'
api_keys = wc_gsbase_api.getApiKeys(secrets_filename)


# Crea conexion API con WooCommerce
wcapi = wc_gsbase_api.getApiParameters(api_keys)

# Leo los JSON de GsBase del directorio input json

for test_filename in os.listdir(directorio_input_json):
    print(test_filename)
    with open(directorio_input_json+test_filename, 'r') as f:
        my_template = json.loads(f.read())


    # Extraigo stock detallado por tallas y colores para cada json

    colores = []
    tallas = []
    resumen_cantidades = []

    for color in my_template["stock"][numero_almacen]:
        cantidades = {}
        colores.append(color)

        for talla in my_template["stock"][numero_almacen][color]:
            if talla not in tallas:
                tallas.append(talla)

            for cantidad in my_template["stock"][numero_almacen][color][talla]:
                pair = {talla: cantidad}
                cantidades.update(pair)

        resumen_cantidades.append(cantidades)

    #Extraigo categorias de gs base y transformo a WC

    categories = [
                {
                    "id": wc_gsbase_api.toWCcategory(my_template["general"]["grupo"])
                },
                {
                    "id": wc_gsbase_api.toWCcategory(my_template["general"]["subgrupo"])
                }
            ]


    # Creo el producto padre para cada color en WC.

    global_sku = ""

    for i in range(len(colores)):

        global_sku = my_template["general"]["codigo"]+colores[i]

        # Datos de las fotos para ese color.

        imagenes = [
            {
                "src": imagenes_src + "105986"+"_"+colores[i]+"_1.png"
            },
            {
                "src": imagenes_src + "105986"+"_"+colores[i]+"_2.png"
            }
        ]

        imported_data = {

            "name": my_template["general"]["denominacion_articulo"]+colores[i],
            "type": "variable",
            "sku": my_template["general"]["codigo"]+colores[i],
            "regular_price": my_template["general"]["pvp"],
            "description": "",
            "short_description": "",
            "categories": categories,
            "images": imagenes,
            "attributes":[
            {
                "id": 1,
                "name": "Talla",
                "position": 0,
                "visible": True,
                "variation": True,
                "options": tallas
            }
        ],
        "default_attributes": [
            {
                "name": "Talla",
                "option": "M"
            }
        ]
    }

        my_json = (wcapi.post("products", imported_data).json())
        print(my_json)



    # Creo las variaciones de las tallas para un color dado.

        my_parent_id = (my_json['id'])
        my_variations = []
        for talla in tallas:

            variation = {
                            "manage_stock": True,
                            "stock_quantity": resumen_cantidades[i][talla],
                            "regular_price": my_template["general"]["pvp"],
                            "sku": global_sku + talla,
                            "attributes": [
                                {
                                    "id": 1,
                                    "option": talla
                                }
                            ]
                        }
            my_variations.append(variation)

        data = {
                "create": my_variations
            }

        wcapi.post("products/"+str(my_parent_id)+"/variations/batch", data).json()

