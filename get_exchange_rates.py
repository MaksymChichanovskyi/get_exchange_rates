import argparse
import json
import random
import requests
import time

from datetime import datetime

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def get_exchange_rates(currencies):
    url = API_URL
    params = {"symbols": ",".join(currencies)}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}")

def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def main(currencies=None):
    if not currencies:
        currencies = random.sample([c for c in ALL_CURRENCIES if c != "USD"], 3)
    for _ in range(3):
        try:
            exchange_rates = get_exchange_rates(currencies)
            break
        except Exception as e:
            print(f"Error: {e}")
            if _ < 2:
                print("Retrying...")
                time.sleep(5)
            else:
                print("Failed to get exchange rates.")
                return

    rates = exchange_rates["rates"]
    data = {"today": {"date": datetime.now().strftime("%A, %B %d, %Y")}}
    data["currencies"] = {}
    for currency in currencies:
        data["currencies"][currency] = {cur: rates[cur] for cur in currencies}
        data["status"] = 200
        data["success"] = True
        
    filename = f"exchange_rates_{datetime.now().strftime('%Y-%m-%d')}.json"
    save_to_json(data, filename)
    print(f"Exchange rates saved to {filename}")

if __name__ == "__main__":
    all_currencies = requests.get(API_URL, params={"symbols": ""}).json()["rates"].keys()
    ALL_CURRENCIES = sorted(all_currencies)
    ALL_CURRENCIES.remove("USD")

    parser = argparse.ArgumentParser(description="Get exchange rates and save them to a JSON file.")
    parser.add_argument(
        "-m",
        "--manual",
        action="store",
        nargs=3,
        metavar=("FIRST_CURRENCY", "SECOND_CURRENCY", "THIRD_CURRENCY"),
        help="Manually specify the currencies to fetch (overrides random selection).",
    )
    args = parser.parse_args()

    if args.manual:
        currencies = args.manual
    else:
        currencies = None

    main(currencies)