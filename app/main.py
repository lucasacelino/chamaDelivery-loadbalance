from fastapi import FastAPI

import socket
import os
import json

with open('pedidos_delivery.json', 'r') as file:
    data = json.load(file)

app = FastAPI(
    title="ChamaDelivery",
    description="API de Gerenciamento de Pedidos Delivery",
)

instance_id = os.getenv("INSTANCE_NUMBER", 'unknow')

@app.get("/pedidos-resturante/{nome_restaurante}")
def getPedidosRestaurante(nome_restaurante: str):
    
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    pedidosRestaunte = []
    for pedido in data:
        if(nome_restaurante == pedido['restaurant']):
            pedidosRestaunte.append(pedido)
            
    return {
        "container_ip": container_ip,
        "instância": instance_id,
        "pedidos": pedidosRestaunte,
        "total": len(pedidosRestaunte)
    }


@app.get("/metodos-pagamentos-pedidos/{tipo_metodo}")
def getPedidosMetPagaments(tipo_metodo: str):
    
    hostname = socket.gethostname()
    container_ip = socket.gethostbyname(hostname)
    
    tiposMetPags = []
    for pedido in data:
        if(tipo_metodo == pedido['payment_method']):
            tiposMetPags.append(pedido)

    return {
        "container_ip": container_ip,
        "instância": instance_id,
        "pedidos": tiposMetPags,
        "total": len(tiposMetPags)
    }
