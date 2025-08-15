# import certificate stores, to handle zscaler
import truststore
truststore.inject_into_ssl()

# import libraries
import requests
import os
from dotenv import load_dotenv
import json
import time

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
            
            # add docket links to each comment
            for comment in comments:
                comment_id = comment.get('id', '')
                if comment_id:
                    # extract docket ID from comment ID (everything before the last hyphen and number)
                    parts = comment_id.split('-')
                    if len(parts) >= 3:
                        docket_id = '-'.join(parts[:-1])
                        # add docket link to the comment's links
                        if 'links' not in comment:
                            comment['links'] = {}
                        comment['links']['docket'] = f"https://www.regulations.gov/docket/{docket_id}"
            
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
        
    print(f"Total comments collected: {len(all_comments)}")
    
    # fetch detailed information for each comment
    print("Fetching detailed information for each comment...")
    
    # Function to handle rate limiting with exponential backoff
    def fetch_with_retry(url, max_retries=5):
        for attempt in range(max_retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limit hit
                    wait_time = (2 ** attempt) * 5  # Exponential backoff: 5, 10, 20, 40, 80 seconds
                    print(f"Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    print(f"HTTP Error {response.status_code}: {response.text}")
                    return response
            except requests.exceptions.RequestException as e:
                wait_time = (2 ** attempt) * 2  # Shorter wait for connection errors
                print(f"Request error: {e}. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
        
        print(f"Failed to fetch after {max_retries} attempts")
        return None
    
    # Process comments with enhanced rate limiting
    for i, comment in enumerate(all_comments, 1):
        comment_id = comment.get('id', '')
        if comment_id:
            # Skip if comment already has detailed info (for resume capability)
            if 'comment' in comment:
                continue
                
            # construct comment detail API call
            comment_url = f"https://api.regulations.gov/v4/comments/{comment_id}?include=attachments&api_key={api_key}"
            comment_detail_response = fetch_with_retry(comment_url)
            
            if comment_detail_response and comment_detail_response.status_code == 200:
                detail_data = comment_detail_response.json()
                comment_detail = detail_data.get('data', {})
                attributes = comment_detail.get('attributes', {})
                
                # append the specific attributes you requested
                if 'commentOn' in attributes:
                    comment['commentOn'] = attributes['commentOn']
                if 'commentOnDocumentId' in attributes:
                    comment['commentOnDocumentId'] = attributes['commentOnDocumentId']
                if 'comment' in attributes:
                    comment['comment'] = attributes['comment']
                if 'firstName' in attributes:
                    comment['firstName'] = attributes['firstName']
                if 'lastName' in attributes:
                    comment['lastName'] = attributes['lastName']
                if 'organization' in attributes:
                    comment['organization'] = attributes['organization']
                if 'email' in attributes:
                    comment['email'] = attributes['email']
                    
                # show progress every 25 comments
                if i % 25 == 0:
                    print(f"Processed {i}/{len(all_comments)} comments...")
                    # save progress
                    temp_data = {
                        "Number of Comments": len(all_comments),
                        "Comments": all_comments
                    }
                    with open('comments_progress.json', 'w', encoding='utf-8') as f:
                        json.dump(temp_data, f, ensure_ascii=False, indent=4)
                
                # delay between requests to avoid rate limiting
                time.sleep(1.0)
                
            else:
                print(f"Failed to fetch details for comment {comment_id}")
                
    print(f"Completed fetching details for all {len(all_comments)} comments.")
        
    # save enhanced comments to json file
    data = {
        "Number of Comments": len(all_comments), # add metadata about the number of comments
        "Comments": all_comments
    }    

    # export to json file
    with open('comments.json', 'w', encoding='utf-8') as f:
       json.dump(data, f, ensure_ascii=False, indent=4) 
       
    print("Comments saved to comments.json") 
        
except requests.exceptions.RequestException as e:
    print(f"Request failed. {e}") # handle request exceptions
    exit(1)
    