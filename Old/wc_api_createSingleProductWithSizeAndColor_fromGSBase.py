#Crea un producto separado por color en WooCommerce desde el JSON de GsBase (SERIE 3). Timeout 60s.

#GET IMAGE BY ID



from woocommerce import API
import json
import time
import wc_gsbase_api

start=time.time()
# Parametros de Importacion.
numero_almacen = "99"
imagenes_src ="https://camanwi.com/imagesResources/"

# Obtengo credenciales API.
secrets_filename = 'secret_keys.json'
api_keys = wc_gsbase_api.getApiKeys(secrets_filename)


# Defino Parametros de Conexion API con WooCommerce
wcapi = wc_gsbase_api.getApiParameters(api_keys)

# Leo el archivo JSON de GsBase
test_filename = 'product_template_filled.json'

with open(test_filename, 'r') as f:
    my_template = json.loads(f.read())


# Extraigo stock detallado por tallas y colores para cada producto
colores = []
tallas = []
resumen_cantidades = []
nombrecolores=[]

for color in my_template["stock"][numero_almacen]:
    cantidades = {}
    colores.append(color)
    nombrecolores.append(wc_gsbase_api.toWCcolor(color))
    for talla in my_template["stock"][numero_almacen][color]:
        if talla not in tallas:
            tallas.append(talla)

        cantidad=(my_template["stock"][numero_almacen][color][talla])
        pair = {talla: cantidad}
        cantidades.update(pair)

    resumen_cantidades.append(cantidades)

print(resumen_cantidades)

#Extraigo categorias de gs base y transformo a WC

categories = [
            {
                "id": wc_gsbase_api.toWCcategory(my_template["general"]["grupo"])
            },
            {
                "id": wc_gsbase_api.toWCcategory(my_template["general"]["subgrupo"])
            }
        ]


# Creo el producto padre en WC.

global_sku = my_template["general"]["codigo"]

# Datos de las fotos para ese color.

images= [
        {
            "id": 1309
        }
    ]

imported_data = {

        "name": my_template["general"]["denominacion_articulo"],
        "type": "variable",
        "sku": my_template["general"]["codigo"]+"V",
        "regular_price": my_template["general"]["pvp"],
        "description": "",
        "short_description": "",
        "images":images,
        "categories": categories,
        "attributes":[
        {
            "id": 1,
            "name": "Talla",
            "position": 0,
            "visible": True,
            "variation": True,
            "options": tallas
        },
        {
            "id": 2,
            "name": "Color",
            "position": 0,
            "visible": True,
            "variation": True,
            "options": nombrecolores
        }

    ],
    "default_attributes": [
        {
            "name": "Talla",
            "option": "M"
        }
    ]
}
print("Comienzo a crear producto padre")
my_json = (wcapi.post("products", imported_data).json())
print(my_json)
time.sleep(0.5)
print("creo producto padre")


# Creo las variaciones de las tallas para un color dado.

my_parent_id = (my_json['id'])
my_variations = []

images_array=[["1300","1301"],["1309","1310"]]


for index, color in enumerate(colores, start=0):

    variation_images = [
        {
            "id": 17031,
            "key": "rtwpvg_images",
            "value": images_array[index][1]
        }
    ]

    for talla in tallas:
        nombrecolor = (wc_gsbase_api.toWCcolor(color))
        variation = {
                        "manage_stock": True,
                        "regular_price": my_template["general"]["pvp"],
                        "stock_quantity": resumen_cantidades[index][talla],
                        "sku": global_sku + "V" + color + talla,
                        "image": {"id":images_array[index][0]},
                        "meta_data": variation_images,
                        "attributes": [
                            {
                                "id": 2,
                                "option": nombrecolor
                            },
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
print("Comienzo a crear productos hijos")
wcapi.post("products/"+str(my_parent_id)+"/variations/batch", data).json()
print("creo productos hijos")
end=time.time()
print(end-start)