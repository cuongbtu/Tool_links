import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urljoin, urlparse

class WebScraperApp:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper Tool")
        master.geometry("700x250")

        self.create_widgets()

    def create_widgets(self):
        entry_width = 50  # Adjust the width according to your preference

        self.label_url = tk.Label(self.master, text="Enter URL: (https://www.examtopics.com/discussions/palo-alto-networks)")
        self.label_url.pack()

        self.url_entry = tk.Entry(self.master, width=entry_width)
        self.url_entry.pack(fill=tk.X, padx=10)

        self.label_start_page = tk.Label(self.master, text="Enter start page number:    (1 : https://www.examtopics.com/discussions/palo-alto-networks/1/)")
        self.label_start_page.pack()

        self.start_page_entry = tk.Entry(self.master, width=entry_width)
        self.start_page_entry.pack(fill=tk.X, padx=10)

        self.label_end_page = tk.Label(self.master, text="Enter end page number:    (5 : https://www.examtopics.com/discussions/palo-alto-networks/5/)")
        self.label_end_page.pack()

        self.end_page_entry = tk.Entry(self.master, width=entry_width)
        self.end_page_entry.pack(fill=tk.X, padx=10)

        self.label_href_pattern = tk.Label(self.master, text="Enter href pattern:   (/discussions/palo-alto-networks/view/)")
        self.label_href_pattern.pack()

        self.href_pattern_entry = tk.Entry(self.master, width=entry_width)
        self.href_pattern_entry.pack(fill=tk.X, padx=10)

        self.scrape_button = tk.Button(self.master, text="Start Scraping", command=self.start_scraping)
        self.scrape_button.pack(pady=5)

    def start_scraping(self):
        url = self.url_entry.get()
        start_page = int(self.start_page_entry.get())
        end_page = int(self.end_page_entry.get())
        href_pattern = self.href_pattern_entry.get()

        if not url:
            print("Please enter a valid URL.")
            return

        # Tạo tên file dựa trên phần cuối của URL
        path_segments = urlparse(url).path.strip('/').split('/')
        base_name = path_segments[-1] if path_segments else 'output'
        file_name = f"{base_name}_all_links.txt"

        driver = webdriver.Edge()  # Update this as per your WebDriver

        with open(file_name, 'w', encoding='utf-8') as output_file:
            for i in range(start_page, end_page + 1):
                page_url = f"{url}/{i}/"
                driver.get(page_url)
                sleep(0.5)

                body_html = driver.find_element(By.TAG_NAME, "body").get_attribute('outerHTML')
                soup = BeautifulSoup(body_html, 'html.parser')

                matching_links = soup.find_all('a', href=lambda href: href and href.startswith(href_pattern))

                for link in matching_links:
                    full_url = link['href'] if link['href'].startswith(('http', 'https')) else urljoin(url, link['href'])
                    output_file.write(full_url + '\n')

                print(f"Finished processing page {i} with {len(matching_links)} links found.")

        driver.quit()
        print(f"All pages processed. Links are saved to {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
