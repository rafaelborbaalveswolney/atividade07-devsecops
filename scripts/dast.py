"""DAST leve: verifica a API executada com requisicoes HTTP reais."""
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000"


def requisicao(path, metodo="GET", dados=None):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(BASE_URL + path, data=data, headers=headers, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=8) as resposta:
            return resposta.status, dict(resposta.headers), resposta.read().decode()
    except urllib.error.HTTPError as erro:
        return erro.code, dict(erro.headers), erro.read().decode()


def conferir(condicao, descricao):
    print(("[OK] " if condicao else "[FALHOU] ") + descricao, flush=True)
    if not condicao:
        sys.exit(1)


status, headers, corpo = requisicao("/health")
conferir(status == 200, "GET /health devolve HTTP 200")
conferir(json.loads(corpo).get("status") == "ok", "Healthcheck valido")
headers = {chave.lower(): valor for chave, valor in headers.items()}
conferir(headers.get("x-content-type-options") == "nosniff", "Header anti-MIME sniffing")
conferir(headers.get("x-frame-options") == "DENY", "Header contra clickjacking")
conferir(headers.get("referrer-policy") == "no-referrer", "Header Referrer-Policy")

status, _, corpo = requisicao("/echo", "POST", {"texto": "teste seguro"})
conferir(status == 200 and json.loads(corpo).get("resposta") == "teste seguro", "POST /echo responde corretamente")
status, _, _ = requisicao("/echo", "POST", {"texto": ""})
conferir(status == 422, "Entrada vazia recusada (422)")
status, _, _ = requisicao("/rota-inexistente")
conferir(status == 404, "Rota inexistente retorna 404")
print("DAST aprovado!", flush=True)
