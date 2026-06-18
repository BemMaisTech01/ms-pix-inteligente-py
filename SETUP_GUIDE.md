# 🔐 Guia de Configuração de Variáveis de Ambiente

## Problema
O arquivo de credenciais do Google Sheets (`pix-inteligente-499220-acd0a7fbcf30.json`) **não pode ser commitado no GitHub** por questões de segurança, mas é necessário localmente.

## Solução

### 1. Instalar python-dotenv
```bash
pip install -r requirements.txt
```
Ou manualmente:
```bash
pip install python-dotenv
```

### 2. Criar arquivo `.env` local
Crie um arquivo chamado `.env` **na raiz do projeto** (próximo ao `main.py`):

```bash
# Copiar do exemplo
copy .env.example .env
```

### 3. Configurar o caminho da credencial
Edite o arquivo `.env` e adicione o **caminho absoluto** para seu arquivo JSON:

**Exemplo Windows:**
```
SHEETS_CREDENTIALS_PATH=C:\Users\seu_usuario\bemmaistech\Projetos\Pix inteligente\ms-pix-inteligente-py\pix-inteligente-499220-acd0a7fbcf30.json
```

**Exemplo Linux/Mac:**
```
SHEETS_CREDENTIALS_PATH=/home/seu_usuario/pix-inteligente-py/pix-inteligente-499220-acd0a7fbcf30.json
```

### 4. Verificar que está funcionando
```bash
python main.py
```

Se vir a mensagem normal de processamento (não erro de credenciais), está pronto!

## ⚠️ IMPORTANTE

- ✅ `.env.example` → **PODE ser commitado** (exemplo sem dados sensíveis)
- ❌ `.env` → **NUNCA fazer commit** (já está em `.gitignore`)
- ❌ `pix-inteligente-499220-acd0a7fbcf30.json` → **NUNCA fazer commit** (já está em `.gitignore`)

## Como funciona

1. O `main.py` carrega o `.env` com `load_dotenv()`
2. A variável `SHEETS_CREDENTIALS_PATH` é lida do `.env`
3. O `Controlador` usa essa variável para conectar ao Google Sheets
4. Funciona sem exposições de chaves no repositório! 🎉

## Para outros devs que clonarem seu projeto

Eles precisam:
1. Obter seu próprio `pix-inteligente-499220-acd0a7fbcf30.json` do Google Cloud
2. Copiar `.env.example` → `.env`
3. Editar o `.env` com o caminho da credencial deles
4. Pronto para usar!

## Troubleshooting

### Erro: "Arquivo de credenciais não encontrado"
- ✅ Verifique se o caminho em `.env` está correto
- ✅ Use caminho **absoluto**, não relativo
- ✅ Verifique se o arquivo JSON realmente existe naquele local

### Erro: "Módulo dotenv não encontrado"
```bash
pip install python-dotenv
```

### Em produção (servidor)
Se usar variáveis de ambiente de sistema:
```bash
# Linux/Mac
export SHEETS_CREDENTIALS_PATH=/path/to/credentials.json

# Windows (PowerShell)
$env:SHEETS_CREDENTIALS_PATH="C:\path\to\credentials.json"

# Docker
ENV SHEETS_CREDENTIALS_PATH=/path/to/credentials.json
```
