import httpx

# List of endpoints to test
urls = [
    "http://127.0.0.1:8000/health"
]

for url in urls:
    response = httpx.get(url)
    assert response.status_code == 200
    print(f"{url} returned 200 OK")
