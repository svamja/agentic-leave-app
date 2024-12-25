FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-slim-bullseye

ENV DOCKER_CONTAINER=true

WORKDIR /app

COPY --from=0 /app .

EXPOSE 8085

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]


