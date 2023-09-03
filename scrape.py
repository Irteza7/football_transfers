import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0\
            (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/91.0.4472.124 Safari/537.36"}

# headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) \
#            Gecko/20100101 Firefox/89.0"}

# URL = "https://www.transfermarkt.com/transfers/saisontransfers/statistik/top/plus/1/galerie/0?saison_id=2023&transferfenster=sommertransfers&land_id=&ausrichtung=&spielerposition_id=&altersklasse=&leihe=&page=1"

URL = "https://www.footballtransfers.com/en/transfers/confirmed/y-2023"

response = requests.get(URL, headers=headers)
for key, value in response.headers.items():
    print(f"{key}: {value}")
soup = BeautifulSoup(response.content, 'html.parser')
row = soup.find_all('tr')[1]  # Get the second row, assuming the first row is the header.
main_table = soup.find("div", class_="responsive-table").find("table", class_="items")

transfers = []
# Iterate through each row in the table body
for row in main_table.tbody.find_all("tr"):
    transfer_info = {}
    
    # Player Name and Profile Link
    player = row.find("a", title=True)
    transfer_info['name'] = player['title']
   
    
    # Age
    age = row.find("td", class_="zentriert").next_sibling.next_sibling
    transfer_info['age'] = age.text.strip()
    
    # Market Value
    market_value = age.next_sibling.next_sibling
    transfer_info['market_value'] = market_value.text.strip()
    
    # Nationality (can be multiple flags, so capturing all in a list)
    flags = market_value.next_sibling.next_sibling.find_all("img", class_="flaggenrahmen")
    transfer_info['nationality'] = [flag['title'] for flag in flags]
    
    # Left Club Name and Link
    left_club = row.find("td", string="Left").find_next("a", title=True)
    transfer_info['left_club_name'] = left_club['title']
    
    # Joined Club Name and Link
    joined_club = row.find("td", string="Joined").find_next("a", title=True)
    transfer_info['joined_club_name'] = joined_club['title']
    
    # Fee
    fee = row.find("td", class_="rechts hauptlink")
    transfer_info['fee'] = fee.text.strip()
    
    # Add the data to our main list
    transfers.append(transfer_info)

# To view the first transfer as an example
print(transfers[0])


# for row in main_table.tbody.find_all("tr"):
#     print(row)


# main_table = soup.select_one('.responsive-table')
# print(str(main_table)[:2000])  # This will print the first 1000 characters of the table.
# header = main_table.select_one('thead')
# print(header)
# sample_row = main_table.select_one('tbody tr')
# print(sample_row)
# main_table.prettify()[:2000]

# match = re.search(r'<td class="hauptlink">\s*<a [^>]*?title="([^"]+)"', str(main_table))
# if match:
#     title = match.group(1)
#     print(title)

# matches = re.findall(r'<td class="hauptlink">\s*<a [^>]*?title="([^"]+)"', str(main_table))

# for match in matches:
#     print(match)


rows = soup.select('.responsive-table .items tbody tr.odd, .responsive-table .items tbody tr.even')
player_data = []

for row in rows:
    player_info = {}

    # Extract Player Name
    name_tag = row.select_one('td.hauptlink a')
    if name_tag:
        player_info['name'] = name_tag.get('title')

    # Extract Age
    age_tag = row.select_one('td.zentriert')
    if age_tag:
        player_info['age'] = age_tag.text.strip()

    # Extract Transfer Cost
    cost_tag = row.select_one('td.rechts')
    if cost_tag:
        player_info['transfer_cost'] = cost_tag.text.strip()

    # Extract Player Position
    position_td = row.select_one('td > table.inline-table > tr:nth-child(2) > td')
    if position_td:
        position = position_td.text.strip()

        # Add the extracted info to the list
    player_data.append(player_info)

print(player_data)

one_row = rows[0]
position_td = one_row.select_one('td > table.inline-table > tr:nth-child(2) > td')
position = position_td.text.strip() if position_td else None


#####################################################
#####################################################

import json
import requests
import pandas as pd
import brotli

base_url = 'https://www.footballtransfers.com/en/transfers/actions/confirmed/overview'

# Use the headers you provided
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

all_records = []
with requests.Session() as session:
    # Set headers to session
    session.headers.update(request_headers)

    for page in range(1, 434):
        post_data = {
            'orderBy': 'date_transfer',
            'orderByDescending': 1,
            'page': page,
            'pages': 415,
            'pageItems': 25,
            'countryId': 'all',
            'year': 2010,
            'tournamentId': 'all',
            'clubFromId': 'all',
            'clubToId': 'all',
            'transferFeeFrom': '',
            'transferFeeTo': ''
        }        
        response = session.post(base_url, data=post_data)
        if response.headers.get('Content-Encoding') == 'br':
            decoded_content = brotli.decompress(response.content)
            data = json.loads(decoded_content.decode('utf-8'))
            records = data['records']
            all_records.extend(records)
        else:
            # handle other encodings or uncompressed data
            data = response.json()
            records = data['records']
            all_records.extend(records)



decoded_content = brotli.decompress(response.content)
print(decoded_content.decode('utf-8'))

df = pd.DataFrame(all_records)
print(df)
df.to_csv('transfers.csv', index=False)