import pandas as pd

def fetch_latest_calendar() -> pd.DataFrame:
    csv_url = "https://raw.githubusercontent.com/kennycornellius-collab/WebScrapper/main/data/usd_high_impact_calendar.csv"
    print(f"Fetching latest macroeconomic data from Repo 1...")
    
    try:
        df = pd.read_csv(csv_url)
        print(f"Successfully loaded {len(df)} high-impact events into memory.")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Make sure the URL is correct and the repository is public.")
        return pd.DataFrame()

if __name__ == "__main__":
    market_data = fetch_latest_calendar()
    if not market_data.empty:
        print("\n--- Market Data Ready for LLM Processing ---")
        print(market_data.to_string())