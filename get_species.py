import requests
from bs4 import BeautifulSoup

import psycopg2


# URL of the page you want to scrape
url = 'https://birdsoftheworld.org/bow/species'

# Send an HTTP request to the URL
response = requests.get(url)
# Ensure the request was successful
response.raise_for_status()

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

print(soup)

species_names = [span.text for span in soup.find_all('span', {'class': 'Heading-main'})]

print(species_names)

print('stuff')
# Database connection parameters
db_params = {
    'dbname': 'birdex',
    'user': 'postgres',
    'host': 'localhost',
    'port': '5431'
}

def insert_species(species_list):
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # SQL to insert a new species
    insert_query = 'INSERT INTO species_list (species_name) VALUES (%s);'

    # Insert each species into the table
    for species in species_list:
        cur.execute(insert_query, (species,))

    # Commit the transaction
    conn.commit()
    
    # Close communication with the database
    cur.close()
    conn.close()

insert_species(species_names)
