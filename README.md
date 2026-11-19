# Atividade 07 - Pipeline DevSecOps

API didatica minima com **Python, FastAPI, Docker, Docker Compose, Kubernetes e GitHub Actions**.
Nao ha banco de dados nem segredo real.

## Executar localmente (Windows / PowerShell)

```powershell
docker compose up -d --build
```

Abrir `http://localhost:8000/docs` ou `http://localhost:8000/health`.

Executar o teste HTTP dinamico:

```powershell
py -3.12 scripts/dast.py
```

Parar:

```powershell
docker compose down
```

## O que a pipeline faz

1. Gitleaks: busca segredos no historico do repositorio.
2. Semgrep: SAST com regras locais e Security Gate (padroes perigosos no codigo).
3. Trivy FS: busca CVEs em dependencias HIGH/CRITICAL.
4. CycloneDX: gera `sbom.cdx.json` com as dependencias.
5. Trivy Config: busca configuracoes inseguras em Dockerfile e Kubernetes.
6. Trivy Image: analisa a imagem Docker e verifica CVEs corrigiveis HIGH/CRITICAL.
7. DAST: sobe a API por Docker Compose e testa os endpoints, validacao e cabecalhos.
8. Deploy: aplicacao e executada no contêiner efemero de CI; nao e publicada em cloud.

Os jobs sao disparados por `push`, Pull Request e manualmente.
Um achado bloqueante reprova a execucao; novos CVEs podem exigir atualizacao de dependencias/base.
O DAST e um script HTTP automatizado (nao e um scanner ZAP completo).

## Demonstracao segura: reprovar e aprovar

Em `app/main.py`, **no final**, adicione temporariamente:

```python
def exemplo_inseguro(entrada: str):
    return eval(entrada)
```

Salve e faca commit/push. O Semgrep deve reprovar a esteira.
Remova a funcao, faca novo commit/push e confira nova execucao.
Nao use chaves ou senhas reais para fazer demonstracoes.

## Arquivos principais

- `app/main.py`: API
- `Dockerfile`: imagem rootless
- `compose.yaml`: container com limitacoes
- `k8s/deployment.yaml`: manifesto IaC de exemplo; nao depende de cluster Kubernetes
- `.github/workflows/devsecops.yml`: esteira
- `.semgrep.yml`: regras locais de SAST
- `scripts/dast.py`: testes dinamicos HTTP
- `requirements.txt`: dependencias

## Entrega

Link de um repositorio publico contendo esses arquivos. A demonstracao e feita na aba Actions do GitHub, no terminal e no navegador, sem slides.
