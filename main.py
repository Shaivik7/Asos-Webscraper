from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox()

driver.get(
    "https://www.asos.com/women/sale/dresses/cat/?cid=5235&ctaref=hp|ww|saleredesign|carousel|1|category|saledresses"
)

product_list = []


def scrape_products():
    products = driver.find_elements(By.CLASS_NAME, "productTile_IAw3u")
    for product in products:
        product_name = product.find_element(
            By.CLASS_NAME, "productDescription_sryaw"
        ).text
        original_price = product.find_element(By.CLASS_NAME, "price__B9LP").text
        reduced_price = product.find_element(By.CLASS_NAME, "reducedPrice_lSm0L").text
        product_link = product.find_element(By.CLASS_NAME, "productLink_P97ZK")

        product_dict = {
            "name": product_name,
            "original_price": original_price,
            "reduced_price": reduced_price,
            "product_link": product_link,
        }
        product_list.append(product_dict)


# Main loop to scrape products and click "load more" until all products are loaded
while True:
    try:
        # Scrape products from the current page
        scrape_products()

        # Check if there's a "load more" button
        load_more_button = driver.find_element(By.CLASS_NAME, "loadButton_wWQ3F")

        # Click the "load more" button
        load_more_button.click()

        # Wait for a moment to let the new products load
        time.sleep(5)
    except NoSuchElementException:
        # If "load more" button is not found, break the loop
        break
    except Exception as e:
        print("An error occurred:", e)
        break

# After all products are loaded, scrape one final time
scrape_products()

df = pd.DataFrame(product_list)
df.to_csv("Asos Products.csv", index=False)
