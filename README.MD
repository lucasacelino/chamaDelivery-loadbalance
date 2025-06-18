# Atividade 2 da Disciplina de Gerência e Configuração de Serviços para Internet 
A segunda atividade de GCSI tem como objetivo configurar um balanceador de carga(load balance) com Nginx usando Docker e posteriormente testar o uso do load balance. O princípio desta atividade é escolher uma aplicação Front(especificamente React) + Back, realizar as ações(requisições), as requisições serão distribuídas entre os nós do load balance. 

Nesta atividade desenvolvi uma aplicação backend utilizando [FastAPI](https://fastapi.tiangolo.com/) - Framework web Python para desenvolver aplicações backend, que simula um sistema de delivery de comida chamado ChamaDelivery. Utilizei um [dataset](/app/pedidos_delivery.json) que contém dados variados sobre pedidos, como: id, tipo de pagamento, restaurante, preço. 

Antes de seguir o passo a passo da configuração, algumas informações precisam ser esclarecidas: 
> É necessário ter o **Docker** e o **Nginx** instalado na sua máquina. Caso não tenha, realize a instalação. 

## Vamos seguir com as seguintes configurações do Backend e Load Balance

**1° passo - Configurar o [Dockerfile](/Dockerfile) da aplicação backend:**
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

**2º Passo - Configurar o arquivo [nginx.conf](/nginx/nginx.conf) para executar o load balance:**
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

o bloco `upstream`- define um grupo de servidores backend para o balanceamento de carga. Cada server refere-se a um serviço definido no docker-compose (os containers fastapi1, fastapi2, etc.).
Todos escutam na porta 8000 (conforme definido nos containers FastAPI).

o bloco `server` - define um servidor virtual que escuta na porta 80 (HTTP padrão).

o bloco `location /` - redireciona todas as requisições para / (ex: http://localhost:8080/) para o grupo de servidores fastapi_servers. 

o bloco `location /docs` - Direciona o caminho /docs diretamente para /docs no backend FastAPI (onde está a documentação Swagger).

o bloco `location /openapi.json` - redireciona para o caminho /openapi.json, onde há um arquivo json com todas as informações da aplicação.


**3º Passo - Configurar o [docker-compose.yaml](/docker-compose.yaml) para criar e gerenciar os contêineres:**

Decidi realizar a configuração dos contêineres através do arquivo docker-compose, pelo fato de facilitar a criação e orquestração de contêiners no Docker em um único arquivo, ao invés, de realizar a configuração via CLI/terminal.

```
version: '3.8'
nginx:
    container_name: loadbalancer_nginx  
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    links:
      - fastapi1
      - fastapi2
      - fastapi3
      - fastapi4
      - fastapi5
    networks:
      - app_net

  fastapi1:
    container_name: fastapi_instance_1  
    build: .
    volumes:
      - ./app:/app
    environment:
      - INSTANCE_NUMBER=1
    expose:
      - "8000"
    networks:
      - app_net

  fastapi2:
    container_name: fastapi_instance_2  
    build: .
    volumes:
      - ./app:/app
    environment:
      - INSTANCE_NUMBER=2
    expose:
      - "8000"
    networks:
      - app_net

  fastapi3:
    container_name: fastapi_instance_3  
    build: .
    volumes:
      - ./app:/app
    environment:
      - INSTANCE_NUMBER=3
    expose:
      - "8000"
    networks:
      - app_net

  fastapi4:
    container_name: fastapi_instance_4  
    build: .
    volumes:
      - ./app:/app
    environment:
      - INSTANCE_NUMBER=4
    expose:
      - "8000"
    networks:
      - app_net

  fastapi5:
    container_name: fastapi_instance_5  
    build: .
    volumes:
      - ./app:/app
    environment:
      - INSTANCE_NUMBER=5
    expose:
      - "8000"
    networks:
      - app_net

networks:
  app_net:
    driver: bridge
```

Explicando cada bloco do docker-compose.yaml:

o bloco `version` - define a versão do docker-compose

o bloco `service`- define todas todas as configurações dos contêineres, como: imagens(image), volumes(volumes), redes(networks) e variávies de ambiente(enviroment).

Por exemplo, o serviço nginx tem os seguintes blocos:

`container_name`- define o nome do contêiner 

`image` - define a imagem do nginx 

`ports` - define a porta de comunicação entre o host e o contêiner docker

`volumes`- Os volumes são sistemas de arquivos montados em contêineres Docker para preservar os dados gerados pelo contêiner. Nesse caso, criei um volume para persistir os dados do `nginx.conf`.

`links`- define uma conexão de rede entre os contêineres vinculados, permitindo que eles se comuniquem entre si.

`networks` - define a rede virtual, na qual, os contêineres irão se comunicar. Nesse caso, o nome da rede que eu criei foi `app_net`.

Bloco dos serviços `fastapi1`, `fastapi2`, etc:

`build`- define a construção de uma imagem **Docker** a partir de um Dockerfile localizado em um determinado diretório.

`enviroment`- define variáveis de ambiente que serão disponibilizadas dentro do contêiner durante sua execução.

`expose`- define que o contêiner usa uma porta internamente (não é exposta para fora). Escuta em uma ou mais portas.


Por fim, para criar os contêiners com base nas imagens definidas do dcoker-compose.yaml, execute o seguinte comando:
```
docker-compose up --build
```

## Testando a aplicação com o Load Balance:
Para finalizar o tutorial, chegamos na parte mais importante, realizar o teste do Load Balance na aplicação Backend. Nessa simples aplicação, desenvolvi apenas 2 endpoints:

`getPedidosRestaurante(nome_restaurante)` - captura todos os pedidos de um respectivo restaurante passado como parâmetro.

`getPedidosMetPagamentos(tipo_metodo)`- captura todos os pedidos de que foram pagos por um método de pagamento específico passado cmo parâmetro.

Para verificar o IP de cada contêiner, execute os seguinte comando:

```
docker network inspect <nome_do_projeto>
```

No caso da apliacação que desenvolvi, cada contêiner/nó tem os seguintes IP's:

```
"Containers": {
            "0004b033bdb075465b9c941e5c3b378a3fd433ef71ef0af46295af88faf327b8": {
                "Name": "fastapi_instance_4",
                "EndpointID": "c7b19c097b05a1d94e5b4f2ccf7ac2a38e14d942e0bfdafbb6357ab06e3355ae",
                "MacAddress": "d6:49:51:10:5e:78",
                "IPv4Address": "172.20.0.3/16",
                "IPv6Address": ""
            },
            "11ea998ff8c8391b64c53552e3674493791fd0b886897c0ab9b91b690d1be2fc": {
                "Name": "fastapi_instance_2",
                "EndpointID": "3655708ac317d074a2a96787cc579669d5472d8c6984bdd9b57e22af245435c2",
                "MacAddress": "a6:81:c7:4b:56:7f",
                "IPv4Address": "172.20.0.2/16",
                "IPv6Address": ""
            },
            "20bd74bbac9ca71c33922ad05d1503d13867822f790088cc88df76e0d7b7a5ca": {
                "Name": "loadbalancer_nginx",
                "EndpointID": "f5f1ed923745eb550fdd89a6e304efb9eb7e2c40baf9ae6a63275c1eaeac43fb",
                "MacAddress": "16:e0:42:98:d6:39",
                "IPv4Address": "172.20.0.7/16",
                "IPv6Address": ""
            },
            "26ec06999f4a08e951dd24c2d47c3e08aed86caa9659dc740adc9074166e84c7": {
                "Name": "fastapi_instance_1",
                "EndpointID": "c84bbdc651616ffae9f61f699c1b9b3073e6475eb0381d707ce0bfd52ec269df",
                "MacAddress": "46:9d:f9:b8:72:84",
                "IPv4Address": "172.20.0.5/16",
                "IPv6Address": ""
            },
            "36f9a4b903944d05aa309817d320ae515871dbdac6f1eed89d7fb5d54c0c634a": {
                "Name": "fastapi_instance_5",
                "EndpointID": "5e3ef2918c1302441ff0b40a405949e1dd02c3c3828743134c9ae3f3dbed6d61",
                "MacAddress": "c6:b0:a7:4d:ad:1c",
                "IPv4Address": "172.20.0.4/16",
                "IPv6Address": ""
            },
            "880a929053649b2d4bd5358aa2bc5a565494de7694174cea16e7780318a30392": {
                "Name": "fastapi_instance_3",
                "EndpointID": "03f4f0e6548b9380cf1c15a9129fd1ef8c83ab9f98497d37faf9b5b36782c07e",
                "MacAddress": "7a:17:f0:c0:43:27",
                "IPv4Address": "172.20.0.6/16",
                "IPv6Address": ""
            }
}
```

**Objetivo - realizar as requisições e verficar qual foi nó(servidor) do load balance que executou a requisição**

Com os contêineres já em execução, acesso a aplicação backend através da URL `http://localhost:8080`. O FastAPI autodocumenta a API desenvolvida no Swagger UI. 
[img-app](/app/images/Captura%20de%20tela%20de%202025-06-16%2014-52-37.png)