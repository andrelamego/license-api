# Dockerfile
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando padrão ao iniciar o container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
