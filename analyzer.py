import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fetcher import fetch_latest_calendar

load_dotenv()

def analyze_macro_environment(df):
    
    if df.empty:
        return "No high-impact data available to analyze."

    
    data_string = df.to_markdown(index=False)

    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    system_instruction = """
    You are the Chief Macroeconomic Analyst for a quantitative hedge fund specializing in XAU/USD (Gold).
    Analyze the provided schedule of high-impact US economic events for the current week.

    Provide your response in exactly two sections:

    ### 1. Pre-Market Briefing
    Write a concise, 2-paragraph summary for a human day trader. 
    - Identify the most dangerous days/times based on the schedule.
    - Briefly explain how the 'Forecast' numbers (e.g., CPI, NFP, Rates) might impact USD strength, and inversely, what that means for Gold.

    ### 2. Algorithmic Risk Flags
    Output a raw JSON block containing risk parameters for a Deep Reinforcement Learning trading bot. 
    Use this EXACT format:
    ```json
    {
      "primary_driver": "String (e.g., Inflation, Employment, Monetary Policy)",
      "expected_volatility": "String (Low, Medium, High, Extreme)",
      "market_regime": "String (e.g., Mean-Reverting, Breakout)",
      "drl_agent_action": "String (e.g., Halt trading 2 hours before [Event Name])"
    }
    ```
    """

    
    prompt = f"Here is the high-impact calendar data for this week:\n\n{data_string}"

    print("Sending data to Google Gemini for analysis")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2 
            )
        )
        return response.text
    except Exception as e:
        return f"API Error: {e}"

if __name__ == "__main__":
    print("Starting AI Macro Analyst Pipeline\n")
    
    market_data = fetch_latest_calendar()
    
    if not market_data.empty:
        analysis = analyze_macro_environment(market_data)
        
        print("\n" + "="*60)
        print("                    MACROECONOMIC REPORT")
        print("="*60 + "\n")
        print(analysis)