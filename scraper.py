import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

print("🚀 GOLD PRICE SCRAPER v3.0 - Sarada Devi Tripathy")
print("Loading Moneycontrol...")

# Moneycontrol gold page
url = "https://www.moneycontrol.com/commodity/mcx-gold-price/"
headers = {'User-Agent': 'Mozilla/5.0'}  # Fake browser
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print("✅ Website loaded! Searching gold price...")

# Method 1: Common price classes try kar
price_classes = ['in-price', 'gld-prc', 'price', 'current-price', 'mc-price', 'rate', 'value']
price = None

for cls in price_classes:
    elements = soup.find_all(['span', 'div', 'td'], class_=re.compile(cls, re.I))
    for elem in elements:
        text = elem.get_text().strip()
        if re.search(r'₹\d+[,.\d]*', text) or '$' in text:
            price = text
            print(f"✅ METHOD 1 SUCCESS: {price} (class: {cls})")
            break
    if price:
        break

# Method 2: ₹ symbol search
if not price:
    for elem in soup.find_all(['span', 'div', 'td']):
        text = elem.get_text().strip()
        if re.search(r'₹\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text) and len(text) < 30:
            price = text
            print(f"✅ METHOD 2 RUPEE SYMBOL: {price}")
            break

# Method 3: Numbers with K/10g
if not price:
    for elem in soup.find_all(text=True):
        if any(word in elem.lower() for word in ['gold', '24k', '10g']) and any(char in elem for char in ['₹', '$']):
            price = elem.strip()
            print(f"✅ METHOD 3 GOLD TEXT: {price}")
            break

if price:
    # Clean price
    price = re.sub(r'[^\d₹$,]', '', price)[:20]
    
    # Save CSV
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"gold_prices_{today[:10]}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['DateTime', 'Gold_Price', 'Source'])
        writer.writerow([today, price, 'Moneycontrol'])
    
    print(f"\n🎉 SUCCESS!")
    print(f"✅ Gold Price: {price}")
    print(f"✅ Saved: {filename}")
else:
    print("❌ Price detection failed. Manual backup data:")
    price = "₹72,450 (24K 10g)"  # Backup
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    filename = f"gold_prices_{today[:10]}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['DateTime', 'Gold_Price', 'Source'])
        writer.writerow([today, price, 'Manual Backup'])
    
    print(f"✅ Backup CSV saved: {filename}")

print("\n🏆 DAY 4 COMPLETE - Gold scraper ready for GitHub!")
