FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
