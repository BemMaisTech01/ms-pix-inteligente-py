FROM python:3.11-slim

WORKDIR /app

# Minimal system dependencies: only poppler for PDF handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and convert to UTF-8 if needed
COPY requirements.txt ./
RUN python - <<'PY'
from pathlib import Path
p = Path('requirements.txt')
text = None
for enc in ('utf-8', 'utf-16'):
    try:
        text = p.read_text(encoding=enc)
        break
    except UnicodeDecodeError:
        continue
if text is None:
    raise RuntimeError('Could not decode requirements.txt with utf-8 or utf-16')
Path('requirements-utf8.txt').write_text(text, encoding='utf-8')
PY

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-utf8.txt

# Copy the rest of the application
COPY . /app

ENV PYTHONUNBUFFERED=1

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "Controller.controlador:app", "--host", "0.0.0.0", "--port", "8000"]
