import os
import re
import json
import requests
from dotenv import load_dotenv
from fetcher import fetch_latest_calendar
from analyzer import analyze_macro_environment

load_dotenv()

def extract_and_save_json(llm_response):
    match = re.search(r'```json\n(.*?)\n```', llm_response, re.DOTALL)
    
    if match:
        json_string = match.group(1)
        try:
            regime_data = json.loads(json_string)

            with open("regime.json", "w") as f:
                json.dump(regime_data, f, indent=4)
            print("Successfully extracted and saved 'regime.json' for the trading bot.")
        except json.JSONDecodeError:
            print("Error: LLM output valid JSON format.")
    else:
        print("Error: Could not find JSON block in LLM response.")

def send_to_discord(llm_response):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("No Discord Webhook URL found in .env file.")
        return
    payload = {
        "content": f"**Weekly Macroeconomic Briefing (XAU/USD)**\n\n{llm_response}"
    }

    print("Broadcasting report to Discord")
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 204:
        print("Successfully pinged Discord")
    else:
        print(f"Failed to send to Discord. Status code: {response.status_code}")

if __name__ == "__main__":
    market_data = fetch_latest_calendar()
    
    if not market_data.empty:

        analysis = analyze_macro_environment(market_data)
        extract_and_save_json(analysis)
        send_to_discord(analysis)