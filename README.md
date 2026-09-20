# B2B Incident Triage Pipeline

An automated support ticket classification pilot built with Python and AWS Bedrock (Claude 3.5 Haiku) to accelerate B2B incident routing.

## Business Value
This system demonstrates how Foundation Models can reduce manual triage bottlenecks by parsing unstructured customer emails and generating strictly structured JSON payloads for downstream IT Service Management (ITSM) databases. It autonomously extracts metadata, categorizes the core issue between (Billing, Technical Support, Sales), and calculates a severity level.

## Architecture & Stack
* **Language:** Python 3.11
* **Cloud AI:** AWS Bedrock (Claude 3.5 Haiku)
* **SDK:** Boto3
* **Infrastructure:** Docker
* **Provisioning:** Designed for seamless multi-platform server deployment via Ansible orchestration.

## Local Deployment

1. **Build the Container:**
   ```bash
   docker build -t b2b-triage-ai .
