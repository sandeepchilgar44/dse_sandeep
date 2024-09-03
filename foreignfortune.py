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

def parse_foreignfortune(html):
    """Parse product information from the HTML content of foreignfortune.com."""
    selector = Selector(text=html)
    products = []

    for product in selector.xpath('//div[@class="grid-view-item product-card"]'):
        title = product.xpath('.//span[contains(@class,"visually-hidden")]/text()').get()
        price = float(product.xpath('.//span[contains(@class, "product-price")]/text()').get().replace('$', ''))
        image = product.xpath('.//img[contains(@class, "image")]/@src').get()
        url = product.xpath('//a[contains(@class,"item__link")]/@href').get()

        products.append({
            "title": title,
            "image": image,
            "price": price,
            "url": url
        })

    return products
async def main():
    """Main function to run the scraping task."""
    url = 'https://foreignfortune.com/collections/men-unisex'
    html = await fetch_page(url)
    products = parse_foreignfortune(html)
    with open('foreignfortune.json', 'w') as f:
        json.dump(products, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
