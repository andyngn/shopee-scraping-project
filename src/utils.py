from bs4 import BeautifulSoup
import time


def extract_data(html, product_data):
    """Function to fetch page's data
    :param html: page source
    :param product_data: structured dataframe for product's data
    """
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all(class_="shopee-search-item-result__item")
    for item in items:
        try:
            link_element = item.select_one("a[data-sqe='link']")
            link = link_element['href'] if link_element else 'No Link'
            name_element = item.select_one(".DgXDzJ.rolr6k.Zvjf4O")
            name = name_element.get_text() if name_element else 'No Name'

            price_elements = item.select(".k9JZlv")
            prices = [float(price.get_text().replace('₫', '').replace('.', '')) for price in price_elements]
            average_price = sum(prices) / len(prices) if prices else 0

            rating_elements = item.select(".shopee-rating-stars__star-wrapper .shopee-rating-stars__lit")
            rating = len(rating_elements)

            sold_element = item.select_one(".OwmBnn.eumuJJ")
            sold_text = sold_element.get_text() if sold_element else '0'
            sold_number = float(sold_text.split(' ')[2].replace('k', '').replace(',', '.')) * 1000 if 'k' in sold_text else float(sold_text.split(' ')[2])

            product_revenue = sold_number * average_price

            product_data['product_name'].append(name)
            product_data['product_url'].append(link)
            product_data['product_price'].append(average_price)
            product_data['product_rating'].append(rating)
            product_data['product_revenue'].append(product_revenue)

        except Exception as e:
            print(f"An error occurred while processing an item: {e}")


def scroll_page(driver, increment=2000, max_attempts=3, wait=5):
    """ Function to imitate scrolling behaviour in a dynamic load website
    :param driver: Chrome driver
    :param increment: increment of each scroll
    :param max_attempts: number of attempts to scroll
    :param wait: delay time in seconds per scroll
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_threshold = last_height * 3 / 4  # Calculate 3/4 of the page height
    attempts = 0

    while True:
        driver.execute_script(f"window.scrollBy(0, {increment});")
        time.sleep(wait)

        new_height = driver.execute_script("return document.body.scrollHeight")
        # Check if we have scrolled 3/4 of the page or reached the bottom
        if new_height >= scroll_threshold or new_height == last_height:
            attempts += 1
            if attempts >= max_attempts:
                print("Reached 3/4 of the page or no more content to load.")
                break
        else:
            attempts = 0  # Reset attempts if new content is loaded

        last_height = new_height


def generate_urls(sub_category_links, pages=9):
    """ Function to generate urls from each sub categories
    :param sub_category_links: list of sub category links
    :param pages: number of scraped page
    """
    urls = []
    for link in sub_category_links:
        for i in range(1, pages + 1):
            urls.append(f'{link}?page={i}')
    return urls

