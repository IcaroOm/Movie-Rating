FROM python:3.10.10
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY . /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]