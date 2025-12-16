import requests
import time

VULN_URL = "http://127.0.0.1:5001/search_vuln"
SECURE_URL = "http://127.0.0.1:5002/search_secure"


def send(url, payload):
    r = requests.post(url, data={'username': payload}, timeout=5)
    return r.text


def analyze_vulnerable(resp):
    if "Explanation:" in resp:
        return "DETECTION"
    if "<table>" in resp:
        return "DATA_LEAK"
    return "NO_EFFECT"


def analyze_secure(resp):
    if "SECURE (BLOCKED)" in resp or "BLOCKED" in resp:
        return "BLOCKED"
    return "ALLOWED"


def main():
    with open('payloads.txt') as f:
        payloads = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    results = []

    for p in payloads:
        print("=" * 60)
        print("Payload:", p)

        try:
            vuln_resp = send(VULN_URL, p)
            secure_resp = send(SECURE_URL, p)
        except Exception as e:
            print("Error contacting app:", e)
            continue

        vuln_result = analyze_vulnerable(vuln_resp)
        secure_result = analyze_secure(secure_resp)

        print("Vulnerable app result:", vuln_result)
        print("Secure app result:", secure_result)

        results.append((p, vuln_result, secure_result))
        time.sleep(0.2)

    print("\nSUMMARY")
    print("-" * 80)
    for p, vuln_res, sec_res in results:
        print(f"{p:45} | vuln: {vuln_res:10} | secure: {sec_res}")


if __name__ == '__main__':
    main()
