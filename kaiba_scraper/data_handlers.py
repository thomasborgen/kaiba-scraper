from typing import List
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup, element


def parse_string_to_soup(raw_html: str) -> BeautifulSoup:
    """Parse html string to BeautifulSoup."""
    return BeautifulSoup(raw_html, 'lxml')


def run_selector(
    html_element: BeautifulSoup,
    css_selector: str,
) -> element.Tag:
    """Find product elements by given css_selector."""
    return html_element.select(css_selector)[0]


def consume_page(url, timeout: int = 10) -> str:
    """Consumes the html as bytes for given url."""
    response = requests.get(url, timeout=timeout)

    if response.ok:
        return response.text


def get_domain_part_of_url(url: str) -> str:
    """Get domain from url."""
    return urlsplit(url).netloc
