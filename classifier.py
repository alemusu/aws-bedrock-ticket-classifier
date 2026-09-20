import csv
import boto3

# boto3 automatically uses the credentials configured via 'aws configure'
client = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

SYSTEM_PROMPT = """You are a B2B support triage AI. Analyze the customer support ticket and classify it.
You MUST respond with valid JSON ONLY. No markdown formatting, no explanation.
Format: {"categoria": "Facturacion|Soporte_Tecnico|Ventas", "nivel_urgencia": 1-5, "resumen_ejecutivo": "..."}"""

def classify_ticket(subject, body):
    prompt = f"Subject: {subject}\nBody: {body}"
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    
    try:
        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            system=[{"text": SYSTEM_PROMPT}]
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        return str(e)

"""Process the example tickets from tickets.csv row by row and print a separator
between them"""
def process_csv():
    with open("tickets.csv", "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            print(f"Processing Ticket #{row['ticket_id']}...")
            result = classify_ticket(row["subject"], row["body"])
            print(f"Result: {result}\n{'-'*40}")

if __name__ == "__main__":
    process_csv()
