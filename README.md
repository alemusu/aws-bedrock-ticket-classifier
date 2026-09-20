# AWS Bedrock B2B Incident Triage Pipeline


## Description
This project is a pilot designed to automate this bottleneck, an automated pipeline designed to go throughput unstructured B2B customer support emails, extract its metadata, and route them using strictly formatted JSON. This pilot demonstrates the integration of Foundation Models into enterprise IT Service Management (ITSM) workflows.

## Process and decision making

### Starting plannification
In B2B customer support, incoming incidents often arrive as messy and unstructured emails. Human agents must manually read these emails, determine if the issue is a billing dispute or a critical system outage, gauge the urgency, and route it to the correct department. This manual triage creates a bottleneck, delaying response times for high-priority outages.

Nowadays we use AI to process this chaotic incoming text and instantly translate it to clean data in for example, a JSON format so that IT systems can automatically route it without human intervention.

Instead of sending the sensitive corporate data to public AI providers we can use AWS Bedrock which acts as a secure gateway to varius AI models. It guarantees that the data remains private inside AWS cloud environment and is not used to train underlying models.

For the specific AI model, I chose Anthropic's Claude 3.5 Haiku over heavier models due to high throughput and mainly, low cost per token. I used AWS billing and cost management to set a 1$ limit notification, but for these trials it used 0.0$. Haiku also excels at zero-shot classification and strict schema adherence (JSON) without the heavier reasoning of other models. 

### AWS Console setup
Before writing any code, the environment required a specific configuration within the AWS Management Console to authorize the API calls:
* **Model access request:** By default, third-party models in Bedrock are locked, so I requested access explicitly to Anthropic models from the "Model access" panel within the Bedrock configuration.
* **Use case submission:** AWS requires a formal declaration of intent to use third-party providers (like Anthropic), so I just specified it would be used for internal software engineering and triague automation, and as "company" I chose independent developper.
* **Permissions**: Once access was granted I ensured my local IAM user credentials, which are mounted in the Docker container, had the necessary bedrock:InvokeModel permissions to communicate with the service.

## Technologies used
* **Language:** Python 3.11 (with standard libraries)
* **AI/ML Infrastructure:** AWS Bedrock with Claude 3.5 Haiku.
* **Cloud SDK:** AWS Boto3.
* **Containerization:** Docker with python:3.11-slim.

## Architecture

### 1. Model Selection: Claude 3.5 Haiku via AWS Bedrock
* **Decision:** Selected Claude 3.5 Haiku
* **Reason:** Ticket triage requires high throughput, low latency, and low cost per token. 

### 2. Output Parsing (Fault tolerant)
* **Decision:** Implemented Regex-based extraction (re.search(r"\{.*\}", raw_text, re.DOTALL)).
* **Reason:** The LLM was "hallucinating" markdown wrappers (```json) or extraneous text. Relying on plain string replacement (like .replace()) caused pipeline failures (JSONDecodeError). The regex approach guarantees that only the serialized JSON object is passed to json.loads(), ensuring deterministic execution.

### 3. Infrastructure & Security
* **Decision:** Containerized via python:3.11-slim with read-only credential mounting.
* **Reason:** The -slim variant reduces the image size and attack surface by stripping unnecessary packages. Authentication is handled by mounting the host's ~/.aws directory as read-only (:ro). This prevents hardcoding static IAM credentials into the container, mimicking secure cloud execution environments where credentials are injected at runtime.

## How does the code work

1. **Initialization:** The script instantiates a boto3 Bedrock client, relying on the environment's IAM configuration.
2. **Data Injection:** Reads incoming support incidents from tickets.csv.
3. **Prompt Construction:** Injects the subject and body into a structured payload. The system prompt forces the LLM to adopt the persona of a routing agent and outputs only a valid JSON.
4. **API Invocation:** Calls the Bedrock Converse API (client.converse()).
5. **Processing:** Strips markdown and validates the structure using the regex.
6. **Output:** Returns a Python dictionary containing "categoria, nivel_urgencia, and resumen_ejecutivo", ready for downstream database insertion.

## Local deployment and testing

**Build the image:**
```bash
docker build -t b2b-triage-ai .
```
The expected output after going through the pilot is a plain text with the tickets from the csv classified correctly by categoria, nivel_urgencia, and resumen_ejecutivo, as explained previously.

