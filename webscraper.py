import requests
from bs4 import BeautifulSoup

def scrape_data(url, r, c):

    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', {'class': 'wikitable'})

    # The FIFA World Cup finals table is the second 'wikitable' table
    world_cup_table = tables[1]

    # Extract rows from the selected table
    rows = world_cup_table.find_all('tr')[1:]  # Skiping header row

    # Define column indices for Year, Winners, Score, and Runners-up
    columns = c # Year, Winners, Score, Runners-up

    # List to store valid rows
    valid_rows = []

    for row in rows:
        if len(valid_rows) >= r:
            break  # Stop once we have 10 valid rows

        cols = row.find_all('td')
        
        # Skipping if the row doesn't have enough columns or data
        if len(cols) < len(columns):
            continue

        try:
            # Extract the Year from the first column
            year = row.find_previous('th') 
            year_text = year.text.strip() if year else None
            int(year_text)
            data = [year_text] + [cols[i].text.strip() for i in columns]  # Getting data from specific columns
            valid_rows.append(data) 
        except Exception:
            continue  # Skipping rows with missing or incomplete data

    # for row in valid_rows:
    #     print(row)
    return valid_rows
