# Python class to grab reputational intelligence from free feeds
import requests, json, sqlite3, os
from datetime import datetime
from typing import List, Dict

class ThreatFreed:
    def __init__(self, config_file: str = "cfg/threat_freed.cfg"):
        self.feeds = self.load_feeds(config_file)
        self.timeout = 15

    def load_feeds(self, config_file: str) -> List[str]:
        feeds = []
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                feeds = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return feeds
    
    # Perform web requests to fetch intelligence/feed information
    def fetch_feeds(self) -> Dict[str, List[str]]:
        threat_data = {}
        
        for url in self.feeds:
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                # create list for each feed key
                content = response.text.strip().split("\n")
                service_name = url.split("/")[2]
                threat_data[service_name] = [line.strip() for line in content if line.strip() and not line.startswith("#")]
            except requests.RequestException as e:
                threat_data[service_name] = {"error": str(e)}
                continue
        
        return threat_data

    # Write results to local disk in json format
    def export_json(self, data: Dict[str, List[str]]):
        os.makedirs("threat_json", exist_ok=True)
        for service, threats in data.items():
            filename = f"threat_json/{service.replace('.', '_')}.json"
            with open(filename, "w") as f:
                json.dump({service: threats}, f, indent=4)

    # Write results to local disk in SQLite format
    def export_database(self, data: Dict[str, List[str]]):
        for service, threats in data.items():
            db_filename = f"threat_dbs/{service.replace('.', '_')}.db"
            conn = sqlite3.connect(db_filename)
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS threats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fetch_date TEXT,
                    threat TEXT
                )
            """)
            fetch_date = datetime.utcnow().isoformat()
            for threat in threats:
                cursor.execute("INSERT INTO threats (fetch_date, threat) VALUES (?, ?)", (fetch_date, threat))
            conn.commit()
            conn.close()

    # Example function that returns json-formatted results
    def get_threat_intel(self) -> str:
        data = self.fetch_feeds()
        return json.dumps(data, indent=4)
    
if __name__ == "__main__":
    try:
        # Constructor requires a max_timeout for web requests
        fetcher = ThreatFreed()

        # Uncomment this to fetch the data feeds and print everything to the terminal
        # If you uncomment data more than once, you will repeatedly fetch the same data unnecessarily
        #data = fetcher.fetch_feeds()
        #print(json.dumps(data, indent=4))

        # Uncomment this to dump feeds to json files under threat_json
        # If you uncomment data more than once, you will repeatedly fetch the same data unnecessarily
        #data = fetcher.fetch_feeds()
        #fetcher.export_json(data)

        # Uncomment this to dump feeds to SQLite dbs under threat_dbs
        # If you uncomment data more than once, you will repeatedly fetch the same data unnecessarily
        #data = fetcher.fetch_feeds()
        #fetcher.export_database(data)
    except Exception as e:
        print(f"Global exception: {e}" )
