import requests
import json
import sys
import time

file_path = sys.argv[1]
retry_count = int(sys.argv[2])
retry_delay = int(sys.argv[3])

results = []
any_failures = False

with open(file_path, "r") as f:
    urls = [u.strip() for u in f.readlines() if u.strip()]

for url in urls:
    status = None
    message = None

    for attempt in range(retry_count):
        try:
            r = requests.get(url, timeout=5)
            status = r.status_code
            message = "OK"
            break
        except Exception as e:
            status = "ERROR"
            message = str(e)
            time.sleep(retry_delay)

    if status != 200:
        any_failures = True

    results.append({
        "url": url,
        "status": status,
        "message": message
    })

# Save results
with open("report.json", "w") as f:
    json.dump(results, f, indent=2)

# Create simple text version
with open("report.txt", "w") as f:
    for r in results:
        f.write(f"{r['url']} - {r['status']} - {r['message']}\n")

print("Validation complete.")

# Fail workflow if any URL failed
if any_failures:
    sys.exit(1)
