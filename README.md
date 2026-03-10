# AI Macro Analyst — Automated Gold Market Intelligence System

## Overview

This is an automated financial intelligence tool that runs every Monday morning before markets open. It pulls live economic calendar data, sends it to an AI model for expert analysis, and broadcasts a professional trading briefing — including risk parameters for an algorithmic trading bot — directly to a Discord channel. The entire pipeline runs hands-free on GitHub's servers with zero manual intervention.

---

## What This Project Does

Every week, major economic events (like US inflation reports, jobs data, or Federal Reserve decisions) cause dramatic price swings in Gold (XAU/USD). Traders need to know *when* these events are happening and *what they mean* before the market opens.

This system automates that entire intelligence workflow:

1. **Fetches** the week's high-impact US economic events from a live data source
2. **Analyzes** them using Google's Gemini AI, prompted to act as a Chief Macroeconomic Analyst
3. **Extracts** structured risk parameters (JSON) for a Deep Reinforcement Learning trading bot
4. **Broadcasts** the full briefing to a Discord channel
5. **Commits** the risk parameters back to the repository for downstream consumption

All of this runs automatically every Monday at 12:30 AM UTC via a GitHub Actions scheduled workflow — no human needed.

---

## Skills Demonstrated

| Area | Detail |
|---|---|
| **AI / LLM Integration** | Prompt engineering with system instructions; structured output extraction from free-form AI responses |
| **API Design** | Google Gemini API (`google-genai`), Discord Webhook API |
| **Data Engineering** | Fetching and parsing live CSV data with `pandas`; markdown formatting for LLM context injection |
| **Automation & DevOps** | GitHub Actions scheduled workflows (CRON), secrets management, automated git commits |
| **Python** | Modular architecture across `fetcher`, `analyzer`, and `notifier` layers |
| **Financial Domain Knowledge** | XAU/USD macro analysis, event-driven volatility, DRL agent risk flagging |

---

## Pipeline

GitHub Actions triggers `notif.py` on a Monday schedule. `fetcher.py` pulls the week's economic calendar into a DataFrame, which `analyzer.py` forwards to Gemini 2.5 Flash with a structured analyst prompt. The response is parsed back in `notif.py` — the JSON block is extracted and committed to the repo as `regime.json`, and the full briefing is posted to Discord.

---

## File Structure

```
.
├── fetcher.py          # Data layer — fetches live economic calendar
├── analyzer.py         # Intelligence layer — Gemini AI analysis
├── notif.py            # Delivery layer — Discord broadcast & JSON extraction
├── regime.json         # Auto-generated risk parameters for the trading bot
└── .github/
    └── workflows/
        └── analyst.yml # Automation — scheduled GitHub Actions workflow
```

---

## Sample AI Output

The system produces two outputs from each run:

**Pre-Market Briefing** (sent to Discord):
> *"This week's primary macro risk centers on Wednesday's CPI release... a hotter-than-expected print would strengthen the USD, applying downward pressure on Gold..."*

**Algorithmic Risk Flags** (saved to `regime.json`):
```json
{
  "primary_driver": "Inflation",
  "expected_volatility": "High",
  "market_regime": "Breakout",
  "drl_agent_action": "Halt trading 2 hours before CPI Release"
}
```

---

## Setup & Configuration

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/)
- A Discord Webhook URL

### Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/kennycornellius-collab/AI-Macro-Analyst.git
cd AI-Macro-Analyst

# 2. Install dependencies
pip install pandas tabulate requests google-genai python-dotenv

# 3. Create a .env file
echo "GEMINI_API_KEY=your_key_here" >> .env
echo "DISCORD_WEBHOOK_URL=your_webhook_here" >> .env

# 4. Run manually
python notif.py
```

### GitHub Actions (Automated)
Add the following secrets to your repository under **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `DISCORD_WEBHOOK_URL` | Your Discord channel webhook URL |

The workflow in `.github/workflows/analyst.yml` will then run automatically every Monday at 12:30 AM UTC. It can also be triggered manually via the **Actions** tab.

---

## Automation Schedule

| Trigger | Time |
|---|---|
| Scheduled (CRON) | Every Monday at 12:30 AM UTC |
| Manual | GitHub Actions → "Run workflow" |


