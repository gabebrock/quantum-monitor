# import certificate stores, to handle zscaler
import truststore
truststore.inject_into_ssl()

# import libraries
import requests
import os
from dotenv import load_dotenv
import json

# load regulations.gov API key from .env.reg
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
searching for all comments that mention 'quantum' AND 'tech'
hoping to reduce number of unrelated results (e.g. 'blood quantum')
"""
base_url = f"https://api.regulations.gov/v4/comments?filter[searchTerm]=quantum AND tech&api_key={api_key}" 

# fetch comments from all pages

all_comments = [] # initialize empty array for data
page = 1
page_size = 250  # maximum allowed by the API

try:
    while True: # while there are more pages (re: page metadata)
        # paginate through api results
        api_url = f"{base_url}&page[size]={page_size}&page[number]={page}"
        print(f"Fetching quantum comments from page {page}...")
        
        response = requests.get(api_url)
    
        if response.status_code == 200: # successful response
            data = response.json()
            comments = data.get('data', [])
            
            if not comments: # when there's no more comments, break loop
                print(f"No more comments found. Stopping at page {page}.")
                break
            
            all_comments.extend(comments)
            print(f"Found {len(comments)} related comments. Subtotal: {len(all_comments)}.")
            
            # see if there's more pages
            meta = data.get('meta', {})
            if 'hasNextPage' in meta and not meta['hasNextPage']:
                print("No more pages found.")
                break
            elif len(comments) < page_size: # if the number of comments on the page is less than the size of the page
                print("Received fewer comments than page size, assuming last page.")
                break
            
            page += 1
                    
        else:
            print(f"Failed to fetch page {page}: {response.status_code} - {response.text}") # print error message
            break
        
    print(f"Found {len(comments)} related comments.")
        
    # save fetched comments to json file
    data = {
        "Number of Comments": len(all_comments),
        "Comments": all_comments
    }    

    # save the fetched data to file
    with open('comments.json', 'w', encoding='utf-8') as f:
       json.dump(data, f, ensure_ascii=False, indent=4) 
       
    print("Comments saved to comments.json") 
        
except requests.exceptions.RequestException as e:
    print(f"Request failed. {e}") # handle request exceptions
    exit(1)
    