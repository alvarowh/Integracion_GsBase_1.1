import json
import time
import wc_gsbase_api
import os

start=time.time()


directorio_input_json = "C:/Users/alvar/Documents/ferrer/Integracion GsBase 1.1/Ficheros GsBase/"
directorio_output_json = "C:/Users/alvar/Documents/ferrer/Integracion GsBase 1.1/Ficheros GsBase/Por Articulo/"

wc_gsbase_api.productSplitJSON(directorio_input_json,directorio_output_json)