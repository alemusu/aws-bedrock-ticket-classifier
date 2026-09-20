#slim bc we don't need the heavier full version
FROM python:3.11-slim 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY classifier.py .
COPY tickets.csv .

CMD ["python", "classifier.py"]
