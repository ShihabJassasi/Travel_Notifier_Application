from dotenv import load_dotenv
import requests, os

load_dotenv()

slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")


def send_slack(text):
    ok = requests.post(slack_webhook_url, json={"text": text})
    return ok.status_code == 200