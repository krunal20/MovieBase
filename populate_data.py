
from elasticsearch import Elasticsearch
import pandas as pd
import json
from config import Config
# Connect to Elasticsearch
es = Elasticsearch(
    Config.get_elasticsearch_url(),
    basic_auth=(Config.ELASTICSEARCH_USER, Config.ELASTICSEARCH_PASSWORD),
    verify_certs=Config.ELASTICSEARCH_VERIFY_CERTS
)

# Read CSV file
def upload_csv_to_elasticsearch(csv_file, index_name):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')
    
    # Upload each record to Elasticsearch
    for i, record in enumerate(records):
        try:
            es.index(index=index_name, id=i, document=record)
        except Exception as e:
            print(f"Error uploading record {i}: {e}")
    
    print(f"Successfully uploaded {len(records)} records to index '{index_name}'")

if __name__ == "__main__":
    # Replace these values with your CSV file path and desired index name
    csv_file = "imdb_top_1000.csv"  # Update this with your CSV file name
    index_name = "imdb_top_1000"  # You can change this index name
    
    # Create the index if it doesn't exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    
    # Upload the data
    upload_csv_to_elasticsearch(csv_file, index_name)