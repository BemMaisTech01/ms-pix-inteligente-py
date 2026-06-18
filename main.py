# Carrega variáveis de ambiente do arquivo .env
from dotenv import load_dotenv

"""
main.py no longer runs local processing. The application is intended to run
as an API (FastAPI app defined in Controller/controlador.py). Start the
server with Uvicorn (this is what the Dockerfile/CMD should do):

  uvicorn Controller.controlador:app --host 0.0.0.0 --port 8000

Local testing (uploads) should be done via the API (Postman, curl, etc.).
"""

load_dotenv()

# Intentionally keep this module minimal — API is served from Controller.controlador

