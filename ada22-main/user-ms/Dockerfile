FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
