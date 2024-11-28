import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


AUTH = 'brd-customer-hl_3da6fe32-zone-webscraper_ai:9kke6f2be7t7'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')

        print("Waiting for captcha...")
        solve_res = driver.execute('executeCdpCommand', {
        'cmd': 'Captcha.waitForSolve',
        'params': {'detectTimeout': 10000}
        })
        print('Captcha Solve Status: ',solve_res['value']['status'])

        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')

        html = driver.page_source
        
        return html



def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if(body):
        return str(body)
    return ""

def clean_body_content(body):
    soup = BeautifulSoup(body, 'html.parser')
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    clean_content = soup.get_text(separator="\n")
    clean_content = "\n".join(line.strip() for line in clean_content.splitlines() if line.strip())
    return clean_content

def split_content(content, size=6000):
    return [content[i:i+size] for i in range(0, len(content), size)]