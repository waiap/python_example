FROM python:3.7

ENV port
ENV host

RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime

RUN pip install poetry
WORKDIR /usr/src/app

COPY poetry.lock /usr/src/app
COPY pyproject.toml /usr/src/app
RUN poetry install --no-dev

COPY . /usr/src/app
RUN poetry install --no-dev

CMD ["poetry", "run", "pwall_aiohttp", "start_server"]

EXPOSE 8080
