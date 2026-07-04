import csv
import time
import requests
from bs4 import BeautifulSoup

for page_num in range(1, 5):
    url = "https://www.scrapethissite.com/pages/forms/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    print("Connecting to the directory server...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # On real directory sites, each business sits inside a uniform table row <tr> or a specific <div> box
        # BUT on this target, every team/company sits inside a table row with class 'team'
        rows = soup.find_all("tr", class_="team")
        
        leads_list = []
        print(f"Found {len(rows)} data entities. Beginning clean extraction...")
        
        for row in rows:
            try:
                # Sifting through real HTML classes precisely
                # .strip() cleans out messy extra spaces and newlines
                name = row.find("td", class_="name").text.strip()
                year = row.find("td", class_="year").text.strip()
                wins = row.find("td", class_="wins").text.strip()
                
                leads_list.append({
                    "Company/Team Name": name,
                    "Established Year": year,
                    "Performance Core/Wins": wins
                })
            except AttributeError:
                continue
                
        # Save
        with open("client_leads.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Company/Team Name", "Established Year", "Performance Core/Wins"])
            writer.writeheader()
            writer.writerows(leads_list)
            
        print(f"Success! Saved {len(leads_list)} rows of clean business data to 'client_leads.csv'.")

    else:
        print(f"Access Denied. Server status code: {response.status_code}")
        
    print(f"Finished parsing page {page_num}")
    time.sleep(2)