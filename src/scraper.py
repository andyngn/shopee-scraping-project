from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils import scroll_page, extract_data


def get_category_links(url='https://shopee.vn/'):
    """ Function to get all the category's url from Shopee """
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        scroll_page(driver)  # Scroll through the page

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        category_elements = soup.find_all(class_='home-category-list__category-grid')

        category_links = [f'https://shopee.vn{link.get("href")}' for link in category_elements]
    finally:
        driver.quit()
    return category_links


def get_sub_category_links(url):
    """ Function to get all sub category's urls from each main category
    :param url: main category's url
    """
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        scroll_page(driver)  # Scroll through the page

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        category_elements = soup.find_all(class_='shopee-category-list__sub-category')

        category_links = [f'https://shopee.vn{link.get("href")}' for link in category_elements]
    finally:
        driver.quit()
    return category_links


def process_page(url, product_data):
    """ Function to process each page by scrolling through the page and fetch data
    :param url: page's url
    :param product_data: item data dataframe
    """
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        scroll_page(driver)
        extract_data(driver.page_source, product_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
