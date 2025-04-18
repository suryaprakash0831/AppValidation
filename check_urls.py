import csv
import requests

def validate_urls(csv_file='urls.csv', report_file='url_report.txt'):
    results = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row['url']
            try:
                response = requests.get(url, timeout=5)
                status = f"{response.status_code} OK" if response.ok else f"{response.status_code} ERROR"
            except Exception as e:
                status = f"ERROR: {str(e)}"
            results.append((url, status))

    with open(report_file, 'w') as f:
        for url, status in results:
            f.write(f"{url} --> {status}\n")

if __name__ == "__main__":
    validate_urls()
