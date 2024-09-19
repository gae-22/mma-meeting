FROM python:3.12-bookworm as builder

WORKDIR /build

COPY . .

RUN pip install --user -r requirements.txt

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /build /app

ENV PATH=/root/.local:$PATH

CMD ["python", "server.py"]
