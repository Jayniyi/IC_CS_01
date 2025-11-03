import requests

# Common payloads
sql_payloads = ["' OR '1'='1", '" OR "1"="1', "';--"]
xss_payloads = ['<script>alert(1)</script>', '" onmouseover="alert(1)"']

def test_sql_injection(url):
    for payload in sql_payloads:
        try:
            response = requests.get(url, params={"q": payload}, timeout=5)
            if "sql" in response.text.lower() or "error" in response.text.lower():
                return True
        except requests.exceptions.RequestException:
            continue
    return False

def test_xss(url):
    for payload in xss_payloads:
        try:
            response = requests.get(url, params={"input": payload}, timeout=5)
            if payload in response.text:
                return True
        except requests.exceptions.RequestException:
            continue
    return False
