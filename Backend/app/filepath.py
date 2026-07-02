import os
import json
from json import JSONDecodeError

VERIFYPATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "database",
    "pending_verifications.json"
)

def getVerifications():
    try:
        with open(VERIFYPATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return {}

def save(data, filepath):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        return f"ERROR: {FileNotFoundError}"