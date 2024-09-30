from dotenv import load_dotenv
load_dotenv()
    
import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


response = supabase.table("producto").select("*").execute()
response = list(response.data)
print(response)
for row in response:
    #row = dict(row)
    print(row.values())