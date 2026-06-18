# 🚀 Guia de Deploy no Render.com

## Problema
Seu arquivo de credenciais JSON não pode ir no GitHub (está em `.gitignore`), então o Render não terá acesso automaticamente.

## Solução: 3 opções

### **Opção 1: Uplocar arquivo JSON direto no Render (RECOMENDADO - FÁCIL)**

1. No painel do Render: `https://dashboard.render.com/project/prj-d8kcstb7uimc73ati150`
2. Vá em **Variáveis de ambiente**
3. Crie uma nova variável:
   - **Chave:** `SHEETS_CREDENTIALS_PATH`
   - **Valor:** deixe em branco por enquanto (vamos usar outra estratégia)

4. **Solução melhor:** Usar variável de ambiente com todo o conteúdo do JSON

### **Opção 2: Usar Variável de Ambiente com JSON completo (MAIS SEGURO)**

1. Abra seu arquivo `pix-inteligente-499220-acd0a7fbcf30.json` localmente
2. Copie **TODO** o conteúdo (é um JSON)
3. No painel do Render, crie uma nova variável:
   - **Chave:** `GOOGLE_CREDENTIALS_JSON` 
   - **Valor:** (Cole o conteúdo inteiro do JSON)

4. Depois, modifique `Controller/controlador.py` para usar essa variável:

```python
import json
import tempfile

def _conectar_sheets(self) -> "gspread.models.Worksheet":
    # Tenta usar arquivo de caminho direto primeiro
    credencial_path = os.environ.get(self.CREDENCIAL_PATH_ENV)
    
    # Se não existir caminho, tenta usar JSON direto
    if not credencial_path:
        google_creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if google_creds_json:
            # Cria arquivo temporário com o JSON
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(google_creds_json)
                credencial_path = f.name
    
    if credencial_path:
        credencial_path = Path(credencial_path)
    else:
        credencial_path = self._diretorio_projeto() / self.CREDENCIAL_SHEETS

    if not credencial_path.exists():
        raise HTTPException(
            status_code=500,
            detail=(
                f"Arquivo de credenciais não encontrado. "
                f"Configure SHEETS_CREDENTIALS_PATH ou GOOGLE_CREDENTIALS_JSON."
            ),
        )
    # ... resto do código igual
```

### **Opção 3: Upload manual no Render (COMPLEXO)**

Usar servidor de arquivos externo para hospedar o JSON (não recomendado por segurança).

---

## ✅ Passos para Deploy (usando Opção 2 - RECOMENDADA)

### 1. Preparar arquivo JSON
```bash
# Leia o arquivo (Windows PowerShell)
Get-Content pix-inteligente-499220-acd0a7fbcf30.json -Raw
```

Copie a saída completa (é um JSON).

### 2. No Painel do Render
- Vá para: https://dashboard.render.com/project/prj-d8kcstb7uimc73ati150
- Clique em seu serviço `ms-pix-inteligente-py`
- Vá em **Environment** (ou **Variáveis de Ambiente**)
- Clique em **Add Environment Variable**
- **Name:** `GOOGLE_CREDENTIALS_JSON`
- **Value:** Cole o JSON inteiro (começando com `{` e terminando com `}`)
- Clique em **Save**

### 3. Fazer commit e push
```bash
git add .
git commit -m "Add Render configuration and environment setup"
git push origin main
```

### 4. Render faz deploy automaticamente

---

## ⚠️ Checklist

- ✅ Arquivo `.env` **NÃO vai para GitHub** (está em `.gitignore`)
- ✅ `requirements.txt` tem `python-dotenv`  
- ✅ `main.py` carrega `load_dotenv()`
- ✅ `Dockerfile` está OK
- ✅ `render.yaml` criado
- ⏳ Variável `GOOGLE_CREDENTIALS_JSON` configurada no Render (fazer agora)

## 🔒 Segurança

- ✅ Credenciais nunca em `.env` no GitHub
- ✅ JSON só no Render (ambiente privado)
- ✅ GitHub não tem acesso às chaves

## Troubleshooting

### Erro: "Arquivo de credenciais não encontrado"
- Verifique se `GOOGLE_CREDENTIALS_JSON` está configurada no Render
- Reinicie o deploy (Manual Deploy)

### Erro: "Invalid JSON"
- Copie o JSON inteiro, sem quebras de linha extras
- No Render, a variável deve começar com `{` e terminar com `}`

### Como testar localmente
```bash
# Copiar valor da variável do Render
# Criar arquivo temporário .env.render
export GOOGLE_CREDENTIALS_JSON='{"tipo": "service_account", ...}'
python main.py
```
