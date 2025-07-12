import json
import csv
import re
from db import insert_log_row, init_db

def parse_text_log_to_db(filepath):
    pattern = r"^(?P<timestamp>[\d\-\s:]+) (?P<level>\w+) (?P<message>.+)$"
    with open(filepath, "r") as f:
        for line in f:
            m = re.match(pattern, line.strip())
            if m:
                insert_log_row(m.group("timestamp"), m.group("level"), m.group("message"))

def parse_json_log_to_db(filepath):
    with open(filepath, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                insert_log_row(data.get("timestamp"), data.get("level"), data.get("message"))
            except:
                pass

def parse_csv_log_to_db(filepath):
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert_log_row(row.get("timestamp"), row.get("level"), row.get("message"))

def load_log_to_db(filepath):
    # Initialize database if it doesn't exist
    init_db()
    if filepath.endswith(".log") or filepath.endswith(".txt"):
        parse_text_log_to_db(filepath)
    elif filepath.endswith(".csv"):
        parse_csv_log_to_db(filepath)
    elif filepath.endswith(".json"):
        parse_json_log_to_db(filepath)
    else:
        raise ValueError("Unsupported file type.")
