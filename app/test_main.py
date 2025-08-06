import datetime
from typing import List
from unittest.mock import patch

# Збережемо оригінальний datetime.date, щоб використовувати у side_effect
_real_date = datetime.date


def make_product(
    name: str, year: int, month: int, day: int, price: int
) -> dict:
    return {
        "name": name,
        "expiration_date": _real_date(year, month, day),
        "price": price,
    }


@patch("app.main.datetime.date")
def test_outdated_products_some(mock_date: "patch") -> None:
    mock_date.today.return_value = _real_date(2022, 2, 2)
    mock_date.side_effect = lambda *args, **kwargs: _real_date(*args, **kwargs)
    products: List[dict] = [
        make_product("salmon", 2022, 2, 10, 600),
        make_product("chicken", 2022, 2, 5, 120),
        make_product("duck", 2022, 2, 1, 160),
    ]
    expected = ["duck"]
    from app.main import outdated_products
    assert outdated_products(products) == expected


@patch("app.main.datetime.date")
def test_outdated_products_none_outdated(mock_date: "patch") -> None:
    mock_date.today.return_value = _real_date(2022, 2, 2)
    mock_date.side_effect = lambda *args, **kwargs: _real_date(*args, **kwargs)
    products: List[dict] = [
        make_product("salmon", 2022, 2, 10, 600),
        make_product("chicken", 2022, 2, 5, 120),
    ]
    expected: List[str] = []
    from app.main import outdated_products
    assert outdated_products(products) == expected


@patch("app.main.datetime.date")
def test_outdated_products_all_outdated(mock_date: "patch") -> None:
    mock_date.today.return_value = _real_date(2022, 2, 10)
    mock_date.side_effect = lambda *args, **kwargs: _real_date(*args, **kwargs)
    products: List[dict] = [
        make_product("salmon", 2022, 2, 1, 600),
        make_product("chicken", 2022, 2, 5, 120),
    ]
    expected = ["salmon", "chicken"]
    from app.main import outdated_products
    assert outdated_products(products) == expected
