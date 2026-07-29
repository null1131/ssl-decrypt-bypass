import json
import urllib.request
import uuid

def fetch_o365_endpoints():
    client_id = str(uuid.uuid4())
    url = f"https://endpoints.office.com/endpoints/WorldWide?clientrequestid={client_id}"
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    urls = set()
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            for entry in data:
                if "urls" in entry:
                    for u in entry["urls"]:
                        urls.add(u.strip().lower())
    except Exception as e:
        print(f"Error fetching O365 endpoints: {e}")
        
    return urls

if __name__ == "__main__":
    urls = fetch_o365_endpoints()
    
    with open("dynamic_o365_fqdn.tmp", "w") as f:
        f.write("\n".join(sorted(urls)))