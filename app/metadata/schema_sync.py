import time
import threading
from app.metadata.schema_loader import save_schema_to_json

SYNC_INTERVAL = 120

def sync_schema():
    while True:
        try:
            save_schema_to_json()
            print(f"Schema synced at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Sync error: {e}")
        time.sleep(SYNC_INTERVAL)

def start_sync_background():
    thread = threading.Thread(target=sync_schema, daemon=True)
    thread.start()
    return thread