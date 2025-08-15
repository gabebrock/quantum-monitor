from dotenv import load_dotenv
import os

def load_api_key(env_file='.env.reg'):
    load_dotenv(env_file)
    return os.getenv('API_KEY')