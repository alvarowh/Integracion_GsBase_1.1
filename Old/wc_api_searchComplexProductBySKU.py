# Busca un producto padre por SKU y devuelve el ID y el SKU de sus hijos (variaciones)

# Si no hay conexion.
# Manera de no tener que extraer todos los productos

from woocommerce import API
import json
import wc_gsbase_api


def searchbySKU(sku):

    # Obtengo las claves
    api_keys = wc_gsbase_api.getApiKeys("secret_keys.json")

    # Crea conexion API con WooCommerce
    if bool(api_keys):

        wcapi = API(
            url="https://camanwi.com",  # Your store URL
            consumer_key=api_keys['WOOCOMMERCE_KEY'],  # Your consumer key
            consumer_secret=api_keys['WOOCOMMERCE_SECRET'],  # Your consumer secret
            wp_api=True,  # Enable the WP REST API integration
            version="wc/v3",  # WooCommerce WP REST API version,
            timeout=15
        )
    else:
        print("No Keys Available")
        exit()

    # Consigue lista de todos los productos (puede que sean solo los 10 ultimos por la pagination)
    my_json = (wcapi.get("products?per_page=50").json())

    # Busca el producto con el sku requerido
    my_products={}
    encontrado=False;

    for attribute in my_json:
        if attribute['sku'] == sku:
            print('Producto Padre ID: ',attribute['id'], 'SKU: ', sku)


            # Busco las variaciones del producto.
            my_variations_id = (attribute['variations'])
            print('Productos hijos ID: ', attribute['variations'])
            encontrado=True
            my_variations_sku = []


    try:
        # Extraigo los detalles de cada variacion a traves de su ID.
        for id in my_variations_id:
            my_product = (wcapi.get("products/"+str(id)).json())
            my_products.update({id: my_product})
            my_variations_sku.append(my_product["sku"])

        resultado=('Productos hijos SKU: ', my_variations_sku)
        # Si encuentra el producto lo guarda en un json.
    except UnboundLocalError as e:
        print(e)
        pass

    if encontrado:
       with open('Retrieved Products Temp.json', 'w') as json_file:
           json.dump(my_products, json_file)
       return resultado
    # Si no lo encuentra
    else:
        resultado=("No se han encontrado productos hijos para el producto " + sku)
        return resultado

