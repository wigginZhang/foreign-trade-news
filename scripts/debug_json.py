import json
import re

with open(r'D:\workspace\foreign-trade-news\data\2026-04-14.json', 'rb') as f:
    raw = f.read()

print("File size:", len(raw))

# Find sections
sections_match = re.search(r'"sections":\s*\[', raw.decode('utf-8', errors='replace'))
if sections_match:
    print("sections found at:", sections_match.start())
    
    # Try to extract sections
    try:
        text = raw.decode('utf-8', errors='replace')
        sections_start = text.find('"sections": [')
        valid_json = '{"sections": [' + text[sections_start + len('"sections": ['):]
        print("Trying to parse sections...")
        data = json.loads(valid_json)
        print("SUCCESS! Found", len(data.get('sections', [])), "sections")
    except Exception as e:
        print("FAILED:", str(e)[:200])
else:
    print("sections not found")
