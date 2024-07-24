FROM python:3.10.2

ARG GIT_COMMIT_HASH="default"
ENV GIT_COMMIT_HASH ${GIT_COMMIT_HASH}

ARG IMAGE_BUILD_DATE="default"
ENV IMAGE_BUILD_DATE ${IMAGE_BUILD_DATE}

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pdm
RUN apt-get update -y
RUN apt-get install -y python3-pil



COPY . /app
RUN pdm self update && pdm install
CMD pdm run localserver
