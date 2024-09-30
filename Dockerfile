FROM python:3.12-bookworm

WORKDIR /app

COPY pyproject.toml .python-version README.md /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl clang libldap2-dev libsasl2-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSLf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
RUN rye sync

COPY datas/ /app/datas/
COPY meeting/ /app/meeting/
COPY server.py .env /app/

CMD ["rye", "run", "python", "server.py"]
