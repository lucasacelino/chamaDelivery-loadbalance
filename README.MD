# Atividade 2 da Disciplina de Gerência e Configuração de Serviços para Internet 
A segunda atividade de GCSI tem como objetivo configurar um balanceador de carga(load balance) com Nginx usando Docker e posteriormente testar o uso do load balance. O princípio desta atividade é escolher uma aplicação Front(especificamente React) + Back, realizar as ações(requisições), as requisições serão distribuídas entre os nós do load balance. 
Nesta atividade desenvolvi uma aplicação backend utilizando FastAPI, que simula um sistema de delivery de comida chamado ChamaDelivery. Utilizei um dataset que contém dados variados sobre pedidos, como: id, tipo de pagamento, restaurante, preço. 
Antes de seguir o passo a passo da configuração, algumas informações precisam ser esclarecidas: 
> É necessário ter o Docker e o Nginx instalado na sua máquina. Caso não tenha, realize a instalação. 
Vamos seguir com as seguintes configurações do Load Balance

1° passo - Configurar o Dockerfile da aplicação backend: