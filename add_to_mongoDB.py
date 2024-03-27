from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

try:
    client = MongoClient(
        "mongodb+srv://vlad:1987@clusterpython.mwbls2w.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPython",
        server_api=ServerApi("1"),
    )
    db_quotes = client.quotes.quotes
    db_authors = client.authors.authors
    print(f"[INFO] Database connected sucsses")
except Exception as e:
    print(f"[INFO] Not connect")
    
    
def add_quotes():
    try:
        with open('quotes.json', 'r', encoding='utf-8') as file:
            quotes = json.load(file)
            db_quotes.insert_many(quotes)  
    except Exception as e :
        print(f'[INFO] Error: {e}')      
        
def add_authors():
    try:
        with open('authors.json', 'r', encoding='utf-8') as file:
            authors = json.load(file)
            db_authors.insert_many(authors)  
    except Exception as e :
        print(f'[INFO] Error: {e}')     
        
        
        
if __name__ == '__main__':
    add_quotes()    
    add_authors()        