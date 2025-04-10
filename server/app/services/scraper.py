import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import asyncio
from datetime import datetime
import uuid

async def scrape_mobile_de(max_price: float, max_mileage: int, radius: int) -> List[Dict]:
    """
    Scrape mobile.de for car listings based on criteria
    """
    base_url = "https://suchen.mobile.de/fahrzeuge/search.html"
    params = {
        "damageUnrepaired": "NO_DAMAGE_UNREPAIRED",
        "isSearchRequest": "true",
        "maxPrice": str(max_price),
        "maxMileage": str(max_mileage),
        "maxPowerAsArray": "PS",
        "minFirstRegistrationDate": "2000-01-01",
        "scopeId": "C",
        "sortOption.sortBy": "searchNetGrossPrice",
        "sortOption.sortOrder": "ASCENDING",
        "usage": "USED",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data: {response.status}")

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            listings = []
            for article in soup.find_all('article', class_='cBox-body--resultitem'):
                try:
                    title = article.find('h3', class_='h3').text.strip()
                    price = float(article.find('div', class_='price-block').text.strip().replace('€', '').replace('.', '').replace(',', '.'))
                    mileage = int(article.find('div', class_='vehicle-data').text.strip().split('km')[0].replace('.', ''))
                    location = article.find('div', class_='rbt-regMilestone').text.strip()
                    url = article.find('a')['href']
                    
                    listing = {
                        'id': str(uuid.uuid4()),
                        'title': title,
                        'price': price,
                        'mileage': mileage,
                        'location': location,
                        'url': url,
                        'created_at': datetime.now().isoformat(),
                    }
                    listings.append(listing)
                except Exception as e:
                    print(f"Error parsing listing: {e}")
                    continue

            return listings 