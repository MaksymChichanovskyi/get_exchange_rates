import argparse
import json
import random
import requests
import time
from datetime import datetime

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


def get_exchange_rates():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}")


def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def main(currencies=None):
    try:
        exchange_rates_data = get_exchange_rates()
        all_currencies = exchange_rates_data["rates"].keys()
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return

    ALL_CURRENCIES = sorted(all_currencies)
    if not currencies:
        currencies = random.sample([c for c in ALL_CURRENCIES if c != "USD"], 3)

    rates = exchange_rates_data["rates"]
    data = {"USD": {currency: rates[currency] for currency in currencies}}

    filename = f"exchange_rates_{datetime.now().strftime('%Y-%m-%d')}.json"
    save_to_json(data, filename)
    print(f"Exchange rates saved to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get exchange rates and save them to a JSON file.")
    parser.add_argument(
        "-m", "--manual",
        action="store",
        nargs="+",
        metavar="CURRENCY",
        help="Manually specify the currencies to fetch (overrides random selection).",
    )
    args = parser.parse_args()

    main(currencies=args.manual)
