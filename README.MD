# Atividade 2 da Disciplina de Gerência e Configuração de Serviços para Internet 
A segunda atividade de GCSI tem como objetivo configurar um balanceador de carga(load balance) com Nginx usando Docker e posteriormente testar o uso do load balance. O princípio desta atividade é escolher uma aplicação Front(especificamente React) + Back, realizar as ações(requisições), as requisições serão distribuídas entre os nós do load balance. 

Nesta atividade desenvolvi uma aplicação backend utilizando [FastAPI](https://fastapi.tiangolo.com/) - Framework web Python para desenvolver aplicações backend, que simula um sistema de delivery de comida chamado ChamaDelivery. Utilizei um [dataset](/app/pedidos_delivery.json) que contém dados variados sobre pedidos, como: id, tipo de pagamento, restaurante, preço. 

Antes de seguir o passo a passo da configuração, algumas informações precisam ser esclarecidas: 
> É necessário ter o **Docker** e o **Nginx** instalado na sua máquina. Caso não tenha, realize a instalação. 

## Vamos seguir com as seguintes configurações do Load Balance

1° passo - Configurar o [Dockerfile](/Dockerfile) da aplicação backend:
```
# Imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos
COPY ./app/requirements.txt /app/requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
