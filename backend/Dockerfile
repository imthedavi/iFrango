# 1. Usa uma imagem oficial, mas a versão "slim" para ser mais leve e segura
FROM python:3.10-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /code

# 3. CRÍTICO: Copia apenas o requirements PRIMEIRO. 
# Isso garante que o Docker use o cache e não reinstale todas as bibliotecas 
# se você apenas alterar uma linha no main.py.
COPY ./requirements.txt /code/requirements.txt

# 4. Instala as dependências sem guardar cache inútil no contêiner
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Só agora copia o resto do seu código
COPY ./app /code/app

# 6. Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]