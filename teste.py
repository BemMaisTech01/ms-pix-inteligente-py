import pandas as pd
import gspread 
from oauth2client.service_account import ServiceAccountCredentials

filename = "pix-inteligente-499220-a11834df3595.json"
scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
             ]
creds = ServiceAccountCredentials.from_json_keyfile_name(filename = filename, scopes = scopes)
client = gspread.authorize(creds)


# Substitua pelo ID real da sua planilha que está na URL do navegador
ID_DA_PLANILHA = "17BijYpzhNVnPurEkcCvs4yrcsHe4hc2XMRM8bX4_-II" 
planilha_completa = client.open_by_key(ID_DA_PLANILHA)

planilha = planilha_completa.get_worksheet(0)  # Acessa a primeira aba da planilha

def mostrar_planilha(planilha):
    """Função para mostrar o conteúdo da planilha."""
    dados = planilha.get_all_records()
    df = pd.DataFrame(dados)
    print(df)

#ler
mostrar_planilha(planilha)

planilha.update_cell(row=2, col=1, value="teste")
mostrar_planilha(planilha)  # Atualiza a célula A2 com o valor "Teste"