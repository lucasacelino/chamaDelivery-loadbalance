# Atividade 2 da Disciplina de Gerência e Configuração de Serviços para Internet 
A segunda atividade de GCSI tem como objetivo configurar um balanceador de carga(load balance) com Nginx usando Docker e posteriormente testar o uso do load balance. O princípio desta atividade é escolher uma aplicação Front(especificamente React) + Back, realizar as ações(requisições), as requisições serão distribuídas entre os nós do load balance. 

Nesta atividade desenvolvi uma aplicação backend utilizando [FastAPI](https://fastapi.tiangolo.com/) - Framework web Python para desenvolver aplicações backend, que simula um sistema de delivery de comida chamado ChamaDelivery. Utilizei um [dataset](/app/pedidos_delivery.json) que contém dados variados sobre pedidos, como: id, tipo de pagamento, restaurante, preço. 

Antes de seguir o passo a passo da configuração, algumas informações precisam ser esclarecidas: 
> É necessário ter o **Docker** e o **Nginx** instalado na sua máquina. Caso não tenha, realize a instalação. 

## Vamos seguir com as seguintes configurações do Backend e Load Balance

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

2º Passo - Configurar o arquivo [nginx.conf](/nginx/nginx.conf) para executar o load balance:
```
events {
    worker_connections 1024;
}

http {
    upstream fastapi_servers {
        server fastapi1:8000;
        server fastapi2:8000;
        server fastapi3:8000;
        server fastapi4:8000;
        server fastapi5:8000;
    }

    server {
        listen 80;
        
        location / {
            proxy_pass http://fastapi_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /docs {
            proxy_pass http://fastapi_servers/docs;
            proxy_set_header Host $host;
        }

        location /openapi.json {
            proxy_pass http://fastapi_servers/openapi.json;
            proxy_set_header Host $host;
        }
    }
}
```
**Explicando cada bloco do ngnix.conf**:

O bloco `events` - define as quantidade de conexões que um worker_process pode lidar simultaneamente. Geralmente o padrão é 1024. É obrigatŕio "setar" esse bloco no nginx.conf.

o bloco `http` - define todas as configurações relacionadas ao tráfego HTTP. Dentro dele é onde define o balanceamento, servidores virtuais (server), rotas (location), etc.

o bloco `upstrem`- define um grupo de servidores backend para o balanceamento de carga. Cada server refere-se a um serviço definido no docker-compose (os containers fastapi1, fastapi2, etc.).
Todos escutam na porta 8000 (conforme definido nos containers FastAPI).

o bloco `server` - define um servidor virtual que escuta na porta 80 (HTTP padrão).

o bloco `location /` - redireciona todas as requisições para / (ex: http://localhost:8080/) para o grupo de servidores fastapi_servers. 

o bloco `location /docs` - 




Decidi realizar a configuração dos contêineres através do arquivo docker-compose pelo o fato de facilitar a criação e orquestração de contêiners no Docker em um único arquivo. 
2º Passo - Configurar o docker-compose.yaml