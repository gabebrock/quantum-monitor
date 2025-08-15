import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Quantum Computing Regulatory Comments",
    page_icon="🔬",
    layout="wide"
)

@st.cache_data
def load_comments():
    """Load and clean comments data"""
    with open('comments_progress.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter valid comments
    valid_comments = []
    for comment in data['Comments']:
        if (comment and 
            isinstance(comment, dict) and 
            comment.get('attributes') and 
            comment['attributes'].get('title') and 
            comment.get('comment')):
            valid_comments.append({
                'id': comment.get('id', ''),
                'title': comment['attributes']['title'],
                'comment': comment['comment'],
                'organization': comment.get('organization', 'Not specified'),
                'agency': comment['attributes'].get('agencyId', ''),
                'posted_date': comment['attributes'].get('postedDate', ''),
                'document_type': comment['attributes'].get('documentType', '')
            })
    
    return pd.DataFrame(valid_comments)

def main():
    st.title("🔬 Quantum Computing Regulatory Comments Dashboard")
    st.markdown("Search and explore regulatory comments on quantum computing technology")
    
    # Load data
    df = load_comments()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Search
    search_term = st.sidebar.text_input("Search comments:", "")
    
    # Agency filter
    agencies = sorted(df['agency'].unique())
    selected_agencies = st.sidebar.multiselect("Select Agencies:", agencies, default=agencies)
    
    # Organization filter
    orgs = sorted(df['organization'].unique())
    selected_orgs = st.sidebar.multiselect("Select Organizations:", orgs[:20])  # Limit for performance
    
    # Apply filters
    filtered_df = df[df['agency'].isin(selected_agencies)]
    
    if selected_orgs:
        filtered_df = filtered_df[filtered_df['organization'].isin(selected_orgs)]
    
    if search_term:
        mask = (
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['comment'].str.contains(search_term, case=False, na=False) |
            filtered_df['organization'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Comments", len(df))
    with col2:
        st.metric("Filtered Comments", len(filtered_df))
    with col3:
        st.metric("Unique Organizations", filtered_df['organization'].nunique())
    
    # Display comments
    st.subheader(f"Comments ({len(filtered_df)})")
    
    for idx, comment in filtered_df.iterrows():
        with st.expander(f"📄 {comment['title'][:100]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Comment:**")
                st.write(comment['comment'][:500] + "..." if len(comment['comment']) > 500 else comment['comment'])
            
            with col2:
                st.write(f"**Organization:** {comment['organization']}")
                st.write(f"**Agency:** {comment['agency']}")
                st.write(f"**ID:** {comment['id']}")
                if comment['posted_date']:
                    try:
                        date = datetime.fromisoformat(comment['posted_date'].replace('Z', '+00:00'))
                        st.write(f"**Posted:** {date.strftime('%Y-%m-%d')}")
                    except:
                        st.write(f"**Posted:** {comment['posted_date']}")

if __name__ == "__main__":
    main()
