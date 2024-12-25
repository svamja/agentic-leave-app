FROM python:3.12-slim-bullseye

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV DOCKER_CONTAINER=true

EXPOSE 8085

CMD ["python", "api/run.py"]


