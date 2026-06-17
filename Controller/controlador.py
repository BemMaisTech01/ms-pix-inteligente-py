import os
import shutil
from pathlib import Path
from typing import Dict, Optional, Union

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi import FastAPI, File, UploadFile, HTTPException

from ocr.image_ocr import ImageOCR
from ocr.separacao_dados import SeparadorDados
from ocr.texto_tratamento import TextoTratamento
from ocr.tratamento_imagem import TratamentoImagem

app = FastAPI()


class Controlador:
    """Controlador que valida e salva o upload no projeto."""

    EXTENCOES_VALIDAS = {".pdf", ".png", ".jpg", ".jpeg", ".img"}
    NOME_SALVO = "imgControlador"
    CREDENCIAL_SHEETS = "pix-inteligente-499220-acd0a7fbcf30.json"
    ID_DA_PLANILHA = "17BijYpzhNVnPurEkcCvs4yrcsHe4hc2XMRM8bX4_-II"
    ABA_INDICE = 0
    CAMPOS = ["banco", "hora", "recebedor", "valor"]
    CREDENCIAL_PATH_ENV = "SHEETS_CREDENTIALS_PATH"

    def __init__(self, arquivo: Union[str, Path, UploadFile]):
        self.upload_file: Optional[UploadFile] = None
        self.caminho_entrada: Optional[Path] = None

        if hasattr(arquivo, "filename") and hasattr(arquivo, "file"):
            self.upload_file = arquivo
            self.suffix = Path(arquivo.filename).suffix.lower()
        else:
            self.caminho_entrada = Path(arquivo)
            self._validar_existencia()
            self.suffix = self.caminho_entrada.suffix.lower()

        self._validar_extensao()
        self.caminho_salvo = self._diretorio_projeto() / f"{self.NOME_SALVO}{self.suffix}"

    def salvar_para_projeto(self) -> str:
        """Salva o arquivo local ou upload no diretório do projeto."""
        if self.upload_file is not None:
            self.upload_file.file.seek(0)
            conteudo = self.upload_file.file.read()
            self.caminho_salvo.write_bytes(conteudo)
        else:
            shutil.copy2(self.caminho_entrada, self.caminho_salvo)
        return str(self.caminho_salvo)

    def _validar_existencia(self) -> None:
        if self.caminho_entrada is None or not self.caminho_entrada.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho_entrada}")

    def _detectar_poppler(self) -> Optional[str]:
        """Retorna o caminho do Poppler se necessário para PDF ou None caso contrário."""
        if self.caminho_salvo.suffix.lower() != ".pdf":
            return None

        if shutil.which("pdfinfo"):
            return None

        poppler_env = os.environ.get("POPPLER_PATH") or os.environ.get("POPLER_PATH")
        if poppler_env and Path(poppler_env).exists():
            return str(poppler_env)

        candidate = Path(r"C:\Users\dener\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin")
        if candidate.exists():
            return str(candidate)

        return None

    def processar_fluxo(self) -> bool:
        """Salva o upload, processa o OCR e exclui o arquivo original no final."""
        caminho_salvo = self.salvar_para_projeto()

        try:
            poppler_path = self._detectar_poppler()
            tratamento_imagem = TratamentoImagem(caminho_salvo, poppler_path=poppler_path)
            imagem_tratada = tratamento_imagem.preprocessar_imagem()

            ocr = ImageOCR()
            texto = ocr.extrair_texto(imagem_tratada)

            linhas = TextoTratamento(texto).process()
            dados = SeparadorDados(linhas).processar()

            self._salvar_planilha(dados)

            # Se quiser inspecionar os dados, pode descomentar abaixo:
            # print('dados extraídos:', dados)

            return True
        finally:
            if Path(caminho_salvo).exists():
                Path(caminho_salvo).unlink()

    def _diretorio_projeto(self) -> Path:
        return Path(__file__).resolve().parents[1]

    def _salvar_planilha(self, dados: Dict[str, Optional[str]]) -> None:
        """Grava os dados extraídos em uma planilha do Google Sheets."""
        planilha = self._conectar_sheets()
        linha = [dados.get(campo, "") or "" for campo in self.CAMPOS]
        planilha.append_row(linha, value_input_option="USER_ENTERED")

    def _conectar_sheets(self) -> "gspread.models.Worksheet":
        credencial_path = os.environ.get(self.CREDENCIAL_PATH_ENV)
        if credencial_path:
            credencial_path = Path(credencial_path)
        else:
            credencial_path = self._diretorio_projeto() / self.CREDENCIAL_SHEETS

        if not credencial_path.exists():
            raise HTTPException(
                status_code=500,
                detail=(
                    f"Arquivo de credenciais não encontrado: {credencial_path}. "
                    f"Defina a variável de ambiente {self.CREDENCIAL_PATH_ENV} ou coloque o arquivo no diretório do projeto."
                ),
            )

        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            filename=str(credencial_path), scopes=scopes
        )
        client = gspread.authorize(creds)
        planilha = client.open_by_key(self.ID_DA_PLANILHA)
        return planilha.get_worksheet(self.ABA_INDICE)

    def _validar_extensao(self) -> None:
        if self.suffix not in self.EXTENCOES_VALIDAS:
            extensoes = ", ".join(sorted(self.EXTENCOES_VALIDAS))
            raise HTTPException(
                status_code=400,
                detail=f"Extensão inválida: {self.suffix}. Use um arquivo com uma das extensões: {extensoes}",
            )


@app.post("/ms-pix-inteligente-py")
async def upload_arquivo(file: UploadFile = File(...)) -> bool:
    """Recebe upload via FastAPI no caminho /ms-pix-inteligente-py, processa o arquivo e retorna True se tudo der certo."""
    controlador = Controlador(file)
    return controlador.processar_fluxo()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Controller.controlador:app", host="0.0.0.0", port=8000, reload=False)
