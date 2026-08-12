# -*- coding: utf-8 -*-
# collector.py
import requests
from database import add_ioc
from datetime import datetime

def fetch_urlhaus():
    print("[+] Fetching data from URLHaus...")
    try:
        response = requests.get("https://urlhaus.abuse.ch/downloads/csv_recent/", timeout=20)
        if response.status_code == 200:
            urls = []
            lines = response.text.splitlines()
            for line in lines:
                if not line.startswith("#") and "," in line:
                    parts = line.split(",")
                    if len(parts) > 2:
                        urls.append(parts[2].strip('"'))
            return [("URLHaus", url) for url in urls]
        else:
            print(f"[!] URLHaus returned status {response.status_code}")
    except Exception as e:
        print(f"[!] Error fetching from URLHaus: {e}")
    return []

def fetch_phishtank():
    print("[+] Fetching data from PhishTank...")
    try:
        response = requests.get("http://data.phishtank.com/data/online-valid.csv", timeout=20)
        if response.status_code == 200:
            urls = []
            lines = response.text.splitlines()
            for line in lines[1:]:  # skip header
                parts = line.split(",")
                if len(parts) > 1:
                    urls.append(parts[1].strip('"'))
            return [("PhishTank", url) for url in urls]
        else:
            print(f"[!] PhishTank returned status {response.status_code}")
    except Exception as e:
        print(f"[!] Error fetching from PhishTank: {e}")
    return []

def fetch_malwarebazaar():
    print("[+] Fetching data from MalwareBazaar...")
    try:
        response = requests.get("https://mb-api.abuse.ch/api/v1/", timeout=20)
        if response.status_code == 200:
            data = response.json()
            urls = []
            if "data" in data:
                for item in data["data"]:
                    urls.append(item.get("sha256", ""))
            return [("MalwareBazaar", url) for url in urls]
        else:
            print(f"[!] MalwareBazaar returned status {response.status_code}")
    except Exception as e:
        print(f"[!] Error fetching from MalwareBazaar: {e}")
    return []

def main():
    all_data = []
    for fetch_func in [fetch_urlhaus, fetch_phishtank, fetch_malwarebazaar]:
        all_data.extend(fetch_func())

    print(f"\n[+] Total collected: {len(all_data)} entries")

    for source, url in all_data:
        if url:
            add_ioc(url, source)

    print("[+] All IOCs saved to database successfully.")

if __name__ == "__main__":
    main()
