FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt update

RUN pip install -r /app/requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY ./models /app/models
COPY ./fastapi_image_predictor.py /app/

RUN useradd -m appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "fastapi_image_predictor:app", "--host", "0.0.0.0", "--port", "8000"]
