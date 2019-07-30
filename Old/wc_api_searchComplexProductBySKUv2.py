# Busca un producto padre por SKU y devuelve el ID y el SKU de sus hijos (variaciones)

# Si no hay conexion.
# Manera de no tener que extraer todos los productos



def getProductList(wcapi,items):

    my_json=(wcapi.get("products?per_page="+str(items)).json())

    return my_json

def searchbySKU(sku, my_json):

    for attribute in my_json:
        if attribute['sku'] == sku:
            if attribute['variations']:
                return attribute['id'],attribute['variations']
            else:
                return attribute['id'],""