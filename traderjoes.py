import asyncio
import os
PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION
from pyppeteer import launch
from parsel import Selector
import json

async def fetch_page(url):
    """Fetch the HTML content of a page."""
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    content = await page.content()
    await browser.close()
    return content
def parse_traderjoes(html):
    """Parse product information from the HTML content of traderjoes.com."""
    selector = Selector(text=html)
    products = []

    for product in selector.xpath('//li[contains(@class, "ProductList_productList")]'):
        print(product)
        title = product.xpath('.//a[contains(@class, "ProductCard_card__title")]/text()').get().strip()
        image = product.xpath('.//img[contains(@class, "ProductCard_card__cover")]/@src').get()
        price = float(product.xpath('.//span[contains(@class, "ProductPrice_productPrice")]/text()').get().strip().replace('$', ''))
        url = product.xpath('.//a/@href').get()

        products.append({
            "title": title,
            "image": image,
            "price": price,
            "url": url
        })

    return products


async def main():
    """Main function to run the scraping task."""
    url = 'https://www.traderjoes.com/home/products/category/wine-beer-liquor-200'
    html = await fetch_page(url)
    products = parse_traderjoes(html)
    with open('traderjoes.json', 'w') as f:
        json.dump(products, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
