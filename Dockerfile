FROM python:3.11-slim


RUN apt-get update && apt-get install -y ffmpeg


WORKDIR /app


COPY . .

RUN pip install -r requirements.txt

EXPOSE 10000


CMD ["gunicorn", "main:app", "-w", "2", "-b", "0.0.0.0:10000"]