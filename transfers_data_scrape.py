import random
import asyncio
import aiohttp
from utils import get_decoded_data, extract_values, desired_fields 


base_url = 'https://www.footballtransfers.com/en/transfers/actions/confirmed/overview'

request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Origin': 'null',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
    'Upgrade-Insecure-Requests': '1'
}

async def fetch(year, page, session):
    post_data = {
        'orderBy': 'date_transfer',
        'orderByDescending': 1,
        'page': page,
        'countryId': 'all',
        'year': year,
        'tournamentId': 'all',
        'clubFromId': 'all',
        'clubToId': 'all',
        'transferFeeFrom': '',
        'transferFeeTo': ''
    }  
    try: 
        async with session.post(base_url, data=post_data) as response:
            content = await response.read()
            data = get_decoded_data(content, response.headers)
            # print(content[:500])
        # Introduce a randomized sleep delay after fetching each page
        await asyncio.sleep(random.uniform(1.0, 5.5))
        return data
    except Exception as e:
        print(f"Error fetching data for year: {year}, page: {page}. Error: {e}")
        return {}




async def fetch_for_year(year, session):
    # Fetch the first page to determine total_pages
    data = await fetch(year, 1, session)
    total_pages = data.get('pages', 1)
    
    # Store the first page
    records = extract_values(data, desired_fields)
    
    # Fetch remaining pages
    tasks = [fetch(year, page, session) for page in range(2, total_pages + 1)]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        records.extend(extract_values(result, desired_fields))
    
    return records



