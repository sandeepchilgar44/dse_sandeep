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

    selector = Selector(text=html)
    products = []

    for product in selector.xpath('//div[contains(@class,"js-product-miniature")]'):
        print("SANDEEP",product)
        title = product.xpath('.//h2[contains(@class, "productMiniature__title")]/text()').get().strip()
        image = product.xpath('.//div[contains(@class,"productMiniature__thumbnails")]//img/@src').get()
        price = product.xpath('.//span[contains(@class, "product-price")]/text()').get().strip().replace('£', '')
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
    url = 'https://www.lechocolat-alainducasse.com/uk/chocolate-bar'
    html = await fetch_page(url)
    products = parse_foreignfortune(html)
    with open('lachocolate.json', 'w') as f:
        json.dump(products, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())