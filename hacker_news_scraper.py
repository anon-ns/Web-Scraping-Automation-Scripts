import csv
import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("Fetching live headlines from Hacker News...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("span", class_="titleline")


# 'newline=""' prevents blank rows between data lines in Excel
with open("hacker_news_headlines.csv", "w", newline="", encoding="utf-8") as file:
   
    fieldnames = ["Index", "Headline"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    
    print(f"Found {len(titles)} headlines. Writing to spreadsheet...")
    
    for index, title in enumerate(titles, 1):
        headline_text = title.a.text
        
       
        writer.writerow({
            "Index": index,
            "Headline": headline_text
        })
        
        # To monitor progress in your terminal
        print(f"Saved: {index}. {headline_text}")

print("\nSuccess! Open 'hacker_news_headlines.csv' to view your spreadsheet.")