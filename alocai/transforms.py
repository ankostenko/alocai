from .consts import ALPHA3_TO_COUNTRY_NAME
from datetime import datetime
from flask import flash


def _release_date_transform(input_date: str) -> str:
    """Transforms release date to required date format

    Args:
        input_date (str): input date to transform(YYYY/MM/DD)

    Returns:
        str: date formatted to required format(DD.MM.YYYY)
    """
    dt = datetime.strptime(input_date, "%Y/%m/%d")
    return dt.strftime("%d.%m.%Y")


def _name_transform(input_name: str) -> str:
    """Transforms name of a game

    Args:
        input_name (str): name of a game(kebab-case)

    Returns:
        str: transformed name a game(Capitalized)
    """

    split = input_name.split('-')

    result = ""
    for part in split:
        result += part.capitalize() + " "

    return result.strip()


def _country_name_transform(input_code: str) -> str:
    """Transforms ISO 3166 alpha-3 country code to country full name

    Args:
        input_code (str): ISO 3166 alpha-3 country code

    Returns:
        str: Country full name
    """
    if input_code not in ALPHA3_TO_COUNTRY_NAME:
        flash(f"Unkown contry code provided {input_code}")
        return "UNKNOWN COUNTRY"

    return ALPHA3_TO_COUNTRY_NAME[input_code]


OUTPUT_COLUMNS = [
    {"output_name": "ID", "transform": None},
    {"output_name": "Release Date", "transform": _release_date_transform},
    {"output_name": "Name", "transform": _name_transform},
    {"output_name": "Country", "transform": _country_name_transform},
    {"output_name": "Copies Sold", "transform": None},
    {"output_name": "Copy Price", "transform": None}
]


OUTPUT_HEADERS = [
    "ID",
    "Release Date",
    "Name",
    "Country",
    "Copies Sold",
    "Copy Price",
    "Total Revenue"
]


COLUMN_NAME_TO_POSITION = {
    "ID": 0,
    "Release Date": 1,
    "Name": 2,
    "Country": 3,
    "Copies Sold": 4,
    "Copy Price": 5,
}
