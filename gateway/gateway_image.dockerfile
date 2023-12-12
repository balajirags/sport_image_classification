FROM python:3.10-slim

RUN pip install pipenv
# Set the working directory in the container
WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "proto.py", "./"]

EXPOSE 9696

CMD ["python", "predict.py", "0.0.0.0:9696"]