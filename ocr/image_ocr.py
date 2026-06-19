import cv2
import numpy as np
import pytesseract
import os

# Use environment variables for Tesseract path when needed.
# In Docker/Render, the executable should be on PATH after `apt-get install -y tesseract-ocr`.
# If you need a custom Tesseract installation path, set TESSERACT_CMD and optionally TESSDATA_PREFIX.

tesseract_cmd = os.environ.get("TESSERACT_CMD")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

if "TESSDATA_PREFIX" in os.environ:
    os.environ["TESSDATA_PREFIX"] = os.environ["TESSDATA_PREFIX"]


class ImageOCR:
    """Classe para extrair texto de uma imagem tratada usando OCR."""

    def __init__(self):
        pass

    def extrair_texto(self, imagem, lang: str = "eng", config: str = "--oem 3 --psm 6") -> str:
        """Extrai texto da imagem tratada usando Tesseract."""
        if imagem is None:
            raise ValueError("Nenhuma imagem fornecida. Use TratamentoImagem para pré-processar a imagem.")

        try:
            texto = pytesseract.image_to_string(imagem, lang=lang, config=config)
        except pytesseract.pytesseract.TesseractError:
            print(f"Aviso: '{lang}' indisponível. Usando OCR padrão.")
            texto = pytesseract.image_to_string(imagem, config=config)

        return texto.strip()

    def OCR(self, imagem, config: str = "--oem 3 --psm 6") -> str:
        """Método público para extrair texto a partir de uma imagem tratada."""
        return self.extrair_texto(imagem, config=config)


if __name__ == "__main__":
    from ocr.tratamento_imagem import TratamentoImagem

    caminho_imagem = "comprovanteNubank.jpeg"
    imagem_tratada = TratamentoImagem(caminho_imagem).preprocessar_imagem()
    texto = ImageOCR().extrair_texto(imagem_tratada)
    print("\n=== TEXTO EXTRAÍDO ===\n")
    print(texto)
