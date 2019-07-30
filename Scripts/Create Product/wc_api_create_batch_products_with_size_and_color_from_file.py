#Crea un producto separado por color en WooCommerce desde el JSON de GsBase (SERIE 3). Timeout 45s.

#Numero variable de imagenes (FTP)
#Informe en texto

import json
import time
import wc_gsbase_api
import os

start=time.time()

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
included_extensions = ['json']
file_names = [fn for fn in os.listdir(directorio_input_json)
              if any(fn.endswith(ext) for ext in included_extensions)]

#REGISTRO DE FALLOS Y EXITOS

succesful_attemps={}
failed_attemps={}

#Intento abrir cada archivo JSON, en caso de no ser posible paso al siguiente.
def createProducts(file_names, images=True):
    for productfile in file_names:
        print("\n")
        print("----------------------------------------------------------------")
        print("Abriendo fichero: "+productfile)
        try:
            with open(directorio_input_json+productfile, 'r') as f:
                my_product = json.loads(f.read())
        except json.decoder.JSONDecodeError as error:
            print (error)
            print("No fue posible abrir el archivo: "+productfile)
            print("\n")
            failed_attemps[productfile]="Fallo de Lectura"
            continue

        # En caso de ser posible abrirlo realizo un chequeo basico de existencia de campos.
        if wc_gsbase_api.basicProductJsonCheck(my_product):

            # Extraigo stock detallado por tallas y colores para el almacen definido en los parametros de importacion.
            resumen_stock, colores, tallas = wc_gsbase_api.getColorsAndSizes(my_product, numero_almacen)

            # Obtengo nombre colores como nombre a partir de codigo de color
            nombrecolores = wc_gsbase_api.toWCcolorList(colores)

            # Extraigo categorias de gs base y transformo a WC
            categories = wc_gsbase_api.getCategories(my_product)

            # Defino la SKU del producto padre
            global_sku = my_product["general"]["codigo"]

            #Defino los recursos de imagenes

            ####################################################
            ####################################################
            #Carga con imagenes
            if images:
                image_resources=wc_gsbase_api.generateImageResources(global_sku,colores,imagenes_src)
            #Carga sin imagenes
            else:
                image_resources=[]
            #Creo estructura JSON para enviar a WooCommerce
            #Informacion para la creacion del producto padre.
            imported_data = {

                    "name": my_product["general"]["denominacion_articulo"],
                    "type": "variable",
                    "sku": my_product["general"]["codigo"],
                    "regular_price": my_product["general"]["pvp"],
                    #"catalog_visibility":"hidden",
                    "description": "",
                    "short_description": "",
                    "images": image_resources,
                    "categories": categories,
                    "attributes":[

                    {
                        "id": 2,
                        "name": "Color",
                        "position": 0,
                        "visible": True,
                        "variation": True,
                        "options": nombrecolores
                    },
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
                            "id": 2,
                            "option": nombrecolores[0]
                        },
                        {

                            "id": 1,
                            "option": tallas[0]
                        }
                ]
            }


            #Envio datos para la creacion de producto a WooCommerce.

            print("Comienzo a crear producto padre SKU:"+global_sku)
            start1=time.time()
            try:
                my_json = (wcapi.post("products", imported_data).json())
            except Exception  as e:
                print(e)
                print("No Fue posible crear el producto: "+global_sku)
                failed_attemps[productfile] = e
                continue
            if wc_gsbase_api.checkProductCreation(my_json):
                print("Producto padre creado en:")
                end1 = time.time()
                print("%.2f" %(end1 - start1))
            else:
                failed_attemps[productfile] = my_json["message"]
                continue

            #Carga con Imagenes
            if images:
                #Reciclo recursos de imagenes creados con el producto padre.
                images_array = wc_gsbase_api.getImagesDetails(my_json)
                if images_array:
                    print("Credas con exito las siguientes imagenes:")
                    print(image_resources)

                else:
                    print("No se han podido crear imagenes para el producto.")


            # Creo los subproductos con las variantes para el producto padre recien creado.
            my_parent_id = (my_json['id'])
            my_variations = []

            for index, color in enumerate(colores, start=0):

                #Color en forma de nombre
                nombrecolor = (wc_gsbase_api.toWCcolor(color))
                #Carga con imagenes
                if images:
                    #Imagen principal de la variacion.
                    main_image = {"id":images_array[3*index][0]}

                    #Imagenes secundarias de la variacion

                    variation_image = [
                        {
                            "key": "rtwpvg_images",
                            "value": [images_array[3*index+1][0],
                                      images_array[3 * index + 2][0]]


                        }
                    ]
                #Carga sin imagenes
                else:
                    main_image=""
                    variation_image=""

                #Genero datos de cada variacion.
                for talla in tallas:


                    variation = {
                                    "manage_stock": True,
                                    "regular_price": my_product["general"]["pvp"],
                                    "stock_quantity": resumen_stock[index][talla],
                                    "sku": global_sku + color + talla,
                                    "image": main_image,
                                    "meta_data": variation_image,
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
                    #Los agrego a la lista de variaciones.
                    my_variations.append(variation)

            #Creo el recurso data para enviar las variaciones
            data = {
                    "create": my_variations
                }
            start2=time.time()
            wcapi.post("products/"+str(my_parent_id)+"/variations/batch", data).json()
            end2=time.time()
            print("Productos hijos creados en:")
            print("%.2f" %(end2-start2))
            succesful_attemps[productfile]="Producto creado SKU:" + global_sku +" ,ID:" + str(my_json['id'])

        else:
            print("El archivo:"+productfile+" no posee los campos basicos para la creacion de productos.")
            failed_attemps[productfile] = "Falta de campos basicos"

createProducts(file_names)

wc_gsbase_api.basicCreationReport(failed_attemps, succesful_attemps)

#Compruebo el fallo en la creacion de producto. Si es por problemas en los recursos de imagenes los creo sin imagenes.

failed_img_attemps=[]
print("\n")
for file in failed_attemps:
    if failed_attemps[file][0:15] =="Imagen no válid" or failed_attemps[file][0:15]=="Error recuperan":
        failed_img_attemps.append(file)
if failed_img_attemps:
    print("Se han encontrado " + str(len(failed_img_attemps)) + " productos no creados por fallos en las imágenes:")
    print(failed_img_attemps)

#Obtengo input del usuario para ver si creo los archivos sin imagenes
    answer = None
    while answer not in ("si", "no"):
        answer = input("¿Quiere crear estos productos sin imagenes? si/no ")
        if answer == "si":
            failed_attemps.clear()
            succesful_attemps.clear()
            createProducts(failed_img_attemps, False)
            wc_gsbase_api.basicCreationReport(failed_attemps,succesful_attemps,False)
        elif answer == "no":
            print("Fin de la creacion de productos.")
        else:
            print("Introduzca si o no para crear productos sin imagenes")
end=time.time()
print("\nTiempo de Ejecucion:"+str("%.2f" %(end-start)))