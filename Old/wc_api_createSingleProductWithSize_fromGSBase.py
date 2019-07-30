#Crea un producto separado por color en WooCommerce desde el JSON de GsBase (SERIE 3). Timeout 30s.

#Comprobar si el producto ya esta creado
#Si falla la creacion del producto padre
#Si no hay conexion



from woocommerce import API
import json
import time
import wc_gsbase_api

# Parametros de Importacion.
numero_almacen = "99"
imagenes_src ="https://camanwi.com/imagesResources/"

# Obtengo credenciales API.
secrets_filename = 'secret_keys.json'
api_keys = {}
with open(secrets_filename, 'r') as f:
    api_keys = json.loads(f.read())


# Crea conexion API con WooCommerce
wcapi = API(
    url="https://camanwi.com", # Your store URL
    consumer_key=api_keys['WOOCOMMERCE_KEY'], # Your consumer key
    consumer_secret=api_keys['WOOCOMMERCE_SECRET'], # Your consumer secret
    wp_api=True, # Enable the WP REST API integration
    version="wc/v3", # WooCommerce WP REST API version
    timeout=30 #timeout
)

# Leo el archivo JSON de GsBase
test_filename = 'product_template_filled.json'

with open(test_filename, 'r') as f:
    my_template = json.loads(f.read())



# Extraigo stock detallado por tallas y colores.

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
            "src": imagenes_src + my_template["general"]["codigo"]+"_"+colores[i]+"_1.png"
        },
        {
            "src": imagenes_src + my_template["general"]["codigo"]+"_"+colores[i]+"_2.png"
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
    time.sleep(1)


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
    time.sleep(1)
