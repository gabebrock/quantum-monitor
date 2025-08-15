from dotenv import load_dotenv
import os
import time
import requests

load_dotenv('.env.reg')

API_KEY = os.getenv('API_KEY')

def fetch_comments(api_key, query, max_pages=10):
    url = "https://api.regulations.gov/v4/comments"
    headers = {"X-Api-Key": api_key}
    all_comments = []
    for page in range(1, max_pages + 1):
        params = {
            "filter[searchTerm]": query,
            "page[size]": 100,
            "page[number]": page
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        comments = [
            {
                "id": item.get("id"),
                "postedDate": item.get("attributes", {}).get("postedDate", ""),
                "title": item.get("attributes", {}).get("title", ""),
                "agencyId": item.get("attributes", {}).get("agencyId", ""),
                "documentType": item.get("attributes", {}).get("documentType", ""),
                "lastModifiedDate": item.get("attributes", {}).get("lastModifiedDate", "")
            }
            for item in data.get("data", [])
        ]
        if not comments:
            break
        all_comments.extend(comments)
    return all_comments

def fetch_comment_details(api_key, comment_id, retries=3, delay=2):
    url = f"https://api.regulations.gov/v4/comments/{comment_id}"
    headers = {"X-Api-Key": api_key}
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:
                print(f"Rate limited for comment {comment_id}. Waiting {delay * (attempt + 1)} seconds...")
                time.sleep(delay * (attempt + 1))
                continue
            response.raise_for_status()
            item = response.json().get("data", {})
            return {
                "id": item.get("id"),
                "commentOnDocumentId": item.get("attributes", {}).get("commentOnDocumentId", ""),
                "comment": item.get("attributes", {}).get("comment", ""),
                "firstName": item.get("attributes", {}).get("firstName", ""),
                "lastName": item.get("attributes", {}).get("lastName", ""),
                "organization": item.get("attributes", {}).get("organization", ""),
                "email": item.get("attributes", {}).get("email", "")
            }
        except requests.exceptions.Timeout:
            print(f"Timeout for comment {comment_id}. Retrying...")
    return None

def fetch_recent_comments(api_key, query, total=1000):
    url = "https://api.regulations.gov/v4/comments"
    headers = {"X-Api-Key": api_key}
    comments = []
    page_size = 100
    pages = total // page_size
    for page in range(1, pages + 1):
        params = {
            "filter[searchTerm]": query,
            "page[size]": page_size,
            "page[number]": page,
            "sort": "-postedDate"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        for item in data.get("data", []):
            comments.append({
                "id": item.get("id"),
                "title": item.get("attributes", {}).get("title", ""),
                "agencyId": item.get("attributes", {}).get("agencyId", ""),
                "documentType": item.get("attributes", {}).get("documentType", ""),
                "postedDate": item.get("attributes", {}).get("postedDate", ""),
                "lastModifiedDate": item.get("attributes", {}).get("lastModifiedDate", "")
            })
        if len(comments) >= total or not data.get("data"):
            break
    print(f"Page {page} response: {data.get('data', [])}")
    return comments[:total]