import pandas as pd
from scraper import get_sub_category_links, process_page, get_category_links
from utils import generate_urls
from concurrent.futures import ThreadPoolExecutor, as_completed


def main(category_list):
    for category_url in category_list:
        category_links = get_sub_category_links(category_url)

        # Generate URLs for the first 10 pages of each sub-category
        urls = generate_urls(category_links)

        product_data = {'product_name': [], 'product_url': [], 'product_price': [], 'product_rating': [], 'product_revenue': []}

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_page, url, product_data): url for url in urls}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"{url} generated an exception: {e}")

        df = pd.DataFrame(product_data)

        # Extract a name from the category URL and use it as the filename
        filename_segment = category_url.split('/')[-1]
        filename = filename_segment.split('-cat.')[0] + '.csv'
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


if __name__ == "__main__":
    category_list = get_category_links()
    main(category_list)
