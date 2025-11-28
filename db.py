import os
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def init_db():
    """
    Initializes and returns a connection to the MongoDB articles collection.
    """
    try:
        # 1. Get credentials from environment variables
        original_password = os.getenv("MONGO_PASSWORD")
        mongo_uri_template = os.getenv("MONGO_URI_TEMPLATE")

        if not original_password or not mongo_uri_template:
            print("Error: MONGO_PASSWORD and MONGO_URI_TEMPLATE must be set in the .env file.")
            return None

        # 2. URL-encode the password and create the connection string
        escaped_password = urllib.parse.quote_plus(original_password)
        mongo_connection_string = mongo_uri_template.replace("{password}", escaped_password)

        # 3. Establish the connection
        client = MongoClient(mongo_connection_string)
        db = client.AsianTripArticles
        articles_collection = db.articles
        
        print("MongoDB connection established successfully.")
        return articles_collection

    except Exception as e:
        print(f"An error occurred during MongoDB connection: {e}")
        return None

# Initialize the collection for global import
articles_collection = init_db()
