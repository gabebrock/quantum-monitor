import pandas as pd

def export_comments_to_csv(comments, filename):
    if comments:
        df = pd.DataFrame(comments)
        df.to_csv(filename, index=False)
    else:
        print("No comments to export.")

def export_details_to_csv(details, filename):
    if details:
        df = pd.DataFrame(details)
        df.to_csv(filename, index=False)
    else:
        print("No details to export.")