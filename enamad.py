import requests as rs
from bs4 import BeautifulSoup
import threading

file_lock = threading.Lock()


def scrape_page(i):
    try:
        get_link = rs.get(f'https://enamad.ir/DomainListForMIMT/Index/{i}').text
        bs = BeautifulSoup(get_link, 'html.parser')

        find_elements = bs.find_all('a', attrs={'class': 'exlink'})

        with file_lock:
            for u in find_elements:
                print(u['href'])
                with open('enamad.txt', 'a') as file:
                    file.write(f'{u["href"]}\n')

    except Exception as exp:
        print(f'error on page {i}: {exp}')


# Run with 10 threads at a time
max_threads = 10
current = 2
end = 6668

while current < end:
    threads = []

    # Start up to max_threads
    for _ in range(max_threads):
        if current < end:
            thread = threading.Thread(target=scrape_page, args=(current,))
            threads.append(thread)
            thread.start()
            current += 1

    # Wait for current batch to finish
    for thread in threads:
        thread.join()

print("All pages processed!")