FROM python:3.11-slim

COPY app /app
WORKDIR /app

RUN python3 -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD uvicorn server:app --host="0.0.0.0" --port=9242

