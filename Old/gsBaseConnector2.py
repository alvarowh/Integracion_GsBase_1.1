import tkinter as tk
import wc_api_checkForNewOrdersv2
import threading
import wc_gsbase_api
import time


#Inicializacón del programa.

window = tk.Tk()
window.title("gsBaseConnector")
window.geometry('950x540')


#DISPLAY DE PEDIDOS

#Frecuencia de la comprobacion
x=10

#Display de texto
pedidos_texto = tk.Text(window, height=10, width=50)
pedidos_texto.grid(column=0,row=6,sticky="nsew")

#Scrollbar
pedidos_scroll = tk.Scrollbar(window, command=pedidos_texto.yview)
pedidos_scroll.grid(column=1, row=6, sticky='nsew')
pedidos_texto['yscrollcommand'] = pedidos_scroll.set


#FUNCIONES PEDIDOS

#Obtengo credenciales:
api_keys = wc_gsbase_api.getApiKeys("secret_keys.json")

#Obtengo parametros de conexion API
wcapi = wc_gsbase_api.getApiParameters(api_keys)

#Obtengo el estado actual de los pedidos.

def getOldOrders():

    orders = wc_api_checkForNewOrdersv2.getOldOrders(wcapi)
    while not orders:
        time.sleep(5)
        orders.clear()
        orders = wc_api_checkForNewOrdersv2.getOldOrders(wcapi)
        pedidos_texto.insert(tk.END, orders)
    return orders

old_orders = getOldOrders()

def checkOrders():

    pedidos = wc_api_checkForNewOrdersv2.getNewOrders(old_orders, wcapi)
    pedidos_texto.insert(tk.END, pedidos)
    threading.Timer(x, checkOrders).start()

checkOrders()


window.mainloop()