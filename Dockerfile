
FROM python:3.12-alpine3.24

# Atualiza o pacote que apresentou vulnerabilidades
RUN apk update \
    && apk upgrade --no-cache krb5-libs

WORKDIR /app

# Instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY app ./app

# Cria um usuário sem privilégios de root
RUN addgroup -S appgroup \
    && adduser -S -G appgroup appuser

USER appuser

EXPOSE 8000

# Verifica se a aplicação está funcionando
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
