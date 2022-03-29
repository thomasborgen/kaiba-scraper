from typing import List, Tuple
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup, element
from soup2dict import convert


def parse_string_to_soup(raw_html_data: str) -> BeautifulSoup:
    """Parse html string to BeautifulSoup."""
    return BeautifulSoup(raw_html_data, 'lxml')


def run_selector(
    html_element: BeautifulSoup,
    css_selector: str,
) -> List[element.Tag]:
    """Find product elements by given css_selector."""
    return html_element.select(css_selector)


def parse_products_to_dict(products: list) -> List[dict]:
    """Parse product html data to dict."""
    return list(map(convert, products))



def consume_page(url, timeout: int = 10) -> requests.Response:
    """Consumes the html as text for given url."""
    response = requests.get(url, timeout=timeout)

    if response.ok:
        return response.text


def get_domain_part_of_url(url: str) -> str:
    """Get domain from url."""
    return urlsplit(url).netloc
