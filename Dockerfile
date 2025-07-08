FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploads/photos /app/uploads/models && \
    chmod -R 777 /app/uploads

ENV PHOTO_FOLDER=/app/uploads/photos
ENV MODEL_FOLDER=/app/uploads/models

EXPOSE 8080

COPY scripts/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
