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