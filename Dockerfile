FROM python:3.12-alpine

WORKDIR /app

ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg

RUN apk add --no-cache gcc musl-dev linux-headers ffmpeg curl && \
    adduser -D appsvc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY ./src .

USER appsvc

CMD ["flask", "run"]
