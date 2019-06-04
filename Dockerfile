FROM openjdk:slim AS allure

MAINTAINER Anatoly Bobunov <dev.bobunov@gmail.com>

FROM python:3.7-slim AS poetry

ENV REPO_NAME pytest_example
ENV REPO_URL https://github.com/AnatolyBobunov/$REPO_NAME.git

RUN apt-get clean && apt-get update \
    && apt-get install -y bash git wget bash python3-dev gcc unzip \
    && git clone -v --progress $REPO_URL $REPO_NAME

WORKDIR /$REPO_NAME

ADD https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py .

RUN POETRY_PREVIEW=1 python3.7 get-poetry.py

ADD pyproject.toml /

ENV PATH="/root/.poetry/bin:$PATH"

RUN pip install --upgrade pip && poetry install --no-interaction --no-ansi

EXPOSE 80

ENV ALLURE_NO_ANALYTICS=1

ARG ALLURE_VERSION=2.12.0
ARG URL=https://dl.bintray.com/qameta/maven/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.zip
ARG INSTALL_DIR=/$REPO_NAME

RUN wget $URL \
    && bash -c "ls -l" \
    && unzip allure-commandline-$ALLURE_VERSION.zip  -d ${INSTALL_DIR} \
    && rm allure-commandline-$ALLURE_VERSION.zip \
    && mv allure-$ALLURE_VERSION allure \
    && ln -s $INSTALL_DIR/allure/bin/allure /usr/bin/allure

VOLUME ["/$REPO_NAME"]

RUN bash -c "ls -l"