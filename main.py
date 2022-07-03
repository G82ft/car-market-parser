import json
import logging
from sys import stdout

import requests
from bs4 import BeautifulSoup

with open('config.json') as config_file:
    CONFIG: dict = json.load(config_file)

HOST: str = 'https://www.auto.ru/'
HEADERS: dict = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    "Accept": '*/*'
}
LOGGER: logging.Logger = logging.getLogger(__name__)


def get_url(region: str = '', type_of_vehicle: str = '', vendor: str = '', model: str = '', age: str = '') -> str:
    if region != 'rossiya':
        LOGGER.warning('Search region is not Russia.')
        LOGGER.debug(f'Region is: {region}.')

    if not region:
        LOGGER.error('Region not specified!')
        LOGGER.warning('Searching in Russia instead.')
        region = 'rossiya'

    region += '/'

    types: tuple[str, ...] = (
        'cars',

        'lcv', 'trailer', 'crane', 'truck', 'agricultural', 'dredge', 'artic', 'construction', 'bulldozers', 'bus',
        'autoloader', 'municipal',

        'motorcycle', 'scooters', 'atv', 'snowmobile',

        'electro'
    )
    if type_of_vehicle not in types:
        LOGGER.error('Incorrect type of vehicle!')
        LOGGER.warning('Searching cars instead.')
    type_of_vehicle += '/'

    vendors_by_region: tuple[str, str] = (
        'vendor-foreign', 'vendor-domestic'
    )
    if vendor:
        if vendor not in vendors_by_region:
            LOGGER.warning('The vendor is not set by region.')
        vendor += '/'
    else:
        vendor = ''

    if model and not vendor:
        LOGGER.error('Model is set, but the vendor is not!')
        LOGGER.warning('Searching without the model.')
        model = ''
    else:
        model += '/'

    ages: tuple[str, str, str] = (
        'all', 'new', 'used'
    )
    if age not in ages:
        LOGGER.error('Incorrect age settings!')
        LOGGER.warning('Searching all instead.')
        age = 'all'
    age += '/'

    return f'{HOST}{region}{type_of_vehicle}{vendor}{model}{age}'


def get_params(params_input: dict) -> dict:
    params_output: dict = {
        "output_type": 'table'
    }

    several_options: dict = {
        "search_tag": (
            'external_panoramas', 'certificate_manufacturer', 'wide-back-seats', 'big', 'handling', 'all-terrain',
            'comfort', 'medium', 'oversize', 'sport', 'economical', 'fast', 'offroad', 'big-trunk', 'compact',
            'new4new', 'style', 'prestige', 'liquid', 'options'
        ),
        "color": (
            '040001', 'CACECB', 'FAFBFB', '97948F', '0000CC', 'EE1D19', '007F00', '200204', 'C49648', '22A0F8',
            'DEA522', '660099', '4A2197', 'FFD600', 'FF8649', 'FFC0CB'
        ),
        "sort": (
            'relevance-asc', 'relevance-desc', 'cr_date-desc', 'cr_date-asc', 'price-acs', 'price-desc',
            'year-desc', 'year-acs', 'km_age-asc', 'km_age-desc', 'alphabet-acs', 'alphabet-desc'
        ),
        "exchange_group": 'POSSIBLE',
        "seller_group": (
            'commercial', 'private'
        ),
        "owners_count_group": (
            'one', 'less_than_two'
        ),
        "steering_wheel": (
            'left', 'right'
        ),
        "transmission": (
            'mechanical', 'automatic', 'robot', 'variator'
        ),
        "pts_status": (
            "1", "2"
        )
    }
    digital_options: tuple[str, ...] = (
        "price_from", "price_to", "year_from", "year_to", "km_age_from", "km_age_to", "displacement_from",
        "displacement_to", "power_from", "power_to", "acceleration_from", "acceleration_to", "fuel_rate_to",
        "clearance_from"
    )
    bool_options: dict = {
        "with_warranty": False,
        "online_view": False,
        "has_image": True,
        "has_video": False
    }

    all_options: tuple = tuple(several_options) + digital_options + tuple(bool_options)

    for key, value in params_input.items():
        key: str
        value: list | str | bool | int

        if key not in all_options or (key not in bool_options and not value):
            LOGGER.debug(f'Option "{key}" skipped. Value: "{value}"')
            continue

        if key in several_options:
            if isinstance(value, list):
                params_output[key] = []
                for i in value:
                    if i not in several_options[key]:
                        LOGGER.warning(f'There is no "{i}" setting in option "{key}". Skipped.')
                        continue
                    params_output[key].append(check_for_upper(key, i))

            else:
                if value not in several_options[key]:
                    LOGGER.warning(f'There is no "{value}" settings in option "{key}". Skipped.')
                    continue
                params_output[key] = check_for_upper(key, value)

        if key in digital_options:
            if not str(value).isdigit():
                LOGGER.warning(f'Only digits allowed for option {key}. Skipped.')
                continue

            params_output[key] = str(value)

        if key in bool_options:
            if not isinstance(value, bool):
                LOGGER.warning(f'Only boolean type is allowed for option {key}. Skipped.')
                continue
            elif bool_options[key] == value:
                LOGGER.debug(f'Option "{key}" has default value ({value}). Skipped.')
                continue

            params_output[key] = str(value).lower()

    return params_output


def check_for_upper(key: str, value: str) -> str:
    upper_settings: tuple[str, ...] = (
        'exchange_group', 'seller_group', 'owners_count_group',
        'steering_wheel', 'transmission'
    )

    if key in upper_settings:
        return str(value).upper()
    else:
        return str(value).lower()


def get_vehicles(url: str, params: dict) -> list:
    vehicles: list = []

    r: requests.Response = requests.get(url, params, headers=HEADERS)

    if not r.ok:
        LOGGER.critical(f'Something went wrong...\nStatus code: {r.status_code}.\nURL: {r.url}.')
        return vehicles

    soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')

    pages: BeautifulSoup = soup.find('span', class_="ListingPagination__pages")

    max_page: int
    if pages is None:
        max_page = 1
    else:
        last_page: int = int(pages.find_all('a', class_="Button")[-1]["href"].split('=')[-1])
        max_page = min(CONFIG["pages"], last_page)

    for p in range(max_page):
        p += 1
        params["p"] = p

        LOGGER.debug(f'URL: {r.url}.')
        LOGGER.info(f'Parsing page {p} of {max_page}...')

        r = requests.get(url, params, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')

        if not r.ok:
            LOGGER.error(f'Something went wrong...\nStatus code: {r.status_code}.\nURL: {r.url}.')
            return vehicles

        table: BeautifulSoup = soup.find('div', class_="ListingCars_outputType_table")

        if table is None:
            LOGGER.error(f'Vehicles not found!')
            return vehicles

        for row in table.find_all('div', class_="ListingItemSequential__enclose"):
            vehicles.append(get_columns(row.contents))

    return vehicles


def get_columns(row) -> dict:
    color, summary, price, km_age, year, engine, place, _ = row

    color = color.div["style"][7:]

    name = summary.text
    price = price.text
    km_age = km_age.text
    year = year.text
    engine = engine.text
    place = place.div.text

    return {
        "color": color,
        "name": name,
        "price": price,
        "km_age": km_age,
        "year": year,
        "engine": engine,
        "place": place
    }


def setup_logger() -> None:
    LOGGER.setLevel(CONFIG["log level"].upper())
    formatter: logging.Formatter = logging.Formatter('[%(levelname)s] %(message)s')
    for handler in (logging.StreamHandler(stdout), logging.FileHandler('parser.log')):
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)


def main():
    setup_logger()

    url: str = get_url(**CONFIG["url"])
    params: dict = get_params(CONFIG["payload"])

    vehicles: list = get_vehicles(url, params)

    with open('vehicles.json') as v:
        json.dump(vehicles, v, indent=2)


main()
