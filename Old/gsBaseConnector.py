import tkinter as tk
from Old import wc_api_searchComplexProductBySKU
import wc_api_checkForNewOrdersv2
import threading
import wc_gsbase_api



#Inicializacón del programa.

window = tk.Tk()
window.title("gsBaseConnector")
window.geometry('950x540')


#BUSQUEDA DE PRODUCTO POR SKU

lbl = tk.Label(window, text="Search By SKU")

lbl.grid(column=0, row=0)

# Parametros de entrada
sku_input_txt = tk.Entry(window, width=10)

sku_input_txt.grid(column=1, row=0)

# Parametros de salida

lbl2 = tk.Label(window, text="Result")

lbl2.grid(column=3, row=0)

# Funcion
def clicked():

    res = wc_api_searchComplexProductBySKU.searchbySKU(sku_input_txt.get())
    lbl2.configure(text=res)

# Boton
btn = tk.Button(window, text="Search", command=clicked)

btn.grid(column=2, row=0)


#DISPLAY DE DE PEDIDOS

#Frecuencia de la comprobacion
x=25

#text display

mytext = tk.Text(window, height=10, width=50)
mytext.grid(column=0,row=6,sticky="nsew")

#scrollbar

scrollb = tk.Scrollbar(window, command=mytext.yview)
scrollb.grid(column=1, row=6, sticky='nsew')
mytext['yscrollcommand'] = scrollb.set

#funciones

api_keys = wc_gsbase_api.getApiKeys("secret_keys.json")

wcapi = wc_gsbase_api.getApiParameters(api_keys)

old_orders = wc_api_checkForNewOrdersv2.getOldOrders(wcapi)


def checkOrders():

    pedidos = wc_api_checkForNewOrdersv2.getNewOrders(old_orders, wcapi)
    mytext.insert(tk.END, pedidos)
    threading.Timer(x, checkOrders).start()

checkOrders()

window.mainloop()
