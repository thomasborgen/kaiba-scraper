import simplejson as json

from kaiba.process import process_raise
from pydantic import BaseModel
from soup2dict import convert

from kaiba_scraper.data_handlers import (
    consume_page,
    get_domain_part_of_url,
    parse_string_to_soup,
    run_selector,
)


class ScraperSettings(BaseModel):
    filename: str
    selector: str


mock_db: dict[str: ScraperSettings] = {
    'www.matprat.no': ScraperSettings(
        filename='matprat.no.json',
        selector='div[class=ingredients-list]',
    ),
    'trinesmatblogg.no': ScraperSettings(
        filename='trinesmatblogg.no.json',
        selector='div[class=single-recipe__ingredients]',
    )
}


def get_db_entry(domain: str) -> ScraperSettings:
    return mock_db.get(domain)


def get_kaiba_configuration(filename: str):

    with open(filename, 'r') as config_file:
        config_data = config_file.read()

    return json.loads(config_data)



def main(url: str):

    # split url to have some sort of key to check in db
    domain = get_domain_part_of_url(url)

    # get the ScraperSettings db entry
    db_entry = get_db_entry(domain)

    # get the kaiba configuration for this url
    kaiba_configuration = get_kaiba_configuration(filename=db_entry.filename)

    # consume page and turn it into soup
    raw_data = consume_page(url)
    soup = parse_string_to_soup(raw_data)

    # select the interesting part of the page
    selected_soup = run_selector(soup, db_entry.selector)

    # convert the soup to a dict
    soup_as_dict = convert(selected_soup)

    # write the raw html json so that its easy to look at while mapping
    with open('raw_html_data.json', 'w') as f:
        f.write(json.dumps(soup_as_dict, ensure_ascii=False))

    # feed the kaiba config and the raw data into the kaiba mapper
    processed_data = process_raise(
        input_data=soup_as_dict,
        configuration=kaiba_configuration,
    )

    # write data:
    with open('mapped_data.json', 'w') as f:
        f.write(json.dumps(processed_data, ensure_ascii=False))


if __name__ == '__main__':
    main(
        url='https://www.matprat.no/oppskrifter/sunn/kyllinggryte-med-gronnsaker/'
    )
