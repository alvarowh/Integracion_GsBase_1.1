import json
import time
import wc_gsbase_api
import os

start=time.time()

# Parametros de Importacion.
directorio_input_json = "C:/Users/alvar/Documents/ferrer/Interactivo_16_07/GsBase/"
productfile="Articulos_2019_07_26_at1.json"
# Leo los JSON de GsBase del directorio input json




with open(directorio_input_json+productfile, 'r') as f:

    my_product = json.loads(f.read())
    colores=(my_product["000001"]["general"]["Colores_Disponibles"])
    for color in colores:
        print(colores.get(color))


