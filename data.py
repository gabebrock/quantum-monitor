import truststore
truststore.inject_into_ssl()

import requests
import os
from dotenv import load_dotenv


# load regulation.gov API key from .env.reg
load_dotenv('.env.reg')
api_key = os.getenv('API_KEY')

if api_key:
    print(f"API Key loaded.") # make sure the key is loaded
else:
    print(f"API Key not found. Rembember to request key. Check env.reg file.") # handle the case where the key is missing
    exit(1)
    
# fetch data from regulation.gov API

"""
assemble search query
searching for all comments that mention 'quantum' AND any of the following terms: 'technolg*', 'comput*', 'sens*', 'communicat*', 'network*
hoping to reduce number of unrelated results (e.g. 'blood quantum')
"""
api_url = f"https://api.regulation.gov/v4/comments?filter[searchTerm]=quantum AND (technolg* OR comput* OR sens* OR communicat* OR network*)&api_key={api_key}" 

# fetch comments
try:
    print(f"Fetching comments from regulation.gov API...")
    response = requests.get(api_url)
    
    if response.status_code == 200: # successful response
        data = response.json()
        comments = data.get('data', [])
        print(f"Found {len(comments)} related comments.")
    else:
        print(f"Failed to fetch comments: {response.status_code} - {response.text}") # print error message

except requests.exceptions.RequestException as e:
    print(f"Request failed. {e}") # handle request exceptions
    exit(1)