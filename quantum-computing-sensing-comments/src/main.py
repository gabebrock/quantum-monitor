import os
import time
import pandas as pd
from utils.env_loader import load_api_key
from api.regulations_api import fetch_recent_comments, fetch_comment_details
from export.csv_exporter import export_comments_to_csv, export_details_to_csv

def main():
    api_key = load_api_key('.env.reg')
    comments_csv = 'quantum_comments.csv'

    # Check if comments CSV exists
    if os.path.exists(comments_csv):
        print(f"Comments already fetched. Loading comments from csv.")
        comments = pd.read_csv(comments_csv).to_dict(orient='records')
    else:
        # Fetch 1000 most recent comments containing "quantum tech"
        comments = fetch_recent_comments(api_key, "quantum tech", total=1000)
        print(f"Fetched {len(comments)} comments")
        export_comments_to_csv(comments, comments_csv)

    # Fetch and export details for each comment
    details = []
    for comment in comments:
        try:
            comment_id = comment.get('id')
            if not comment_id:
                print("Comment missing 'id', skipping:", comment)
                continue
            detail = fetch_comment_details(api_key, comment_id)
            if detail:
                details.append(detail)
            time.sleep(1)  # Add delay to avoid rate limiting
        except Exception as e:
            print(f"Error fetching details for comment: {comment}. Error: {e}")

    print(f"Fetched details for {len(details)} comments")
    export_details_to_csv(details, 'quantum_comments_details.csv')

if __name__ == "__main__":
    main()