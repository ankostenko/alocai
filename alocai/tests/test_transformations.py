
from alocai import OUTPUT_COLUMNS
from alocai.transforms import (_name_transform, _release_date_transform,
                               _country_name_transform)


def test_only_some_columns_has_transform_funcs():
    """
        Test that only release date, name and country code has transform funcs.
    """
    expected_columns = ["Release Date", "Name", "Country"]

    for column in OUTPUT_COLUMNS:
        if column['transform'] and column['output_name'] not in expected_columns:
            assert False


def test_name_transform_func():
    """
        Tests name transformations
    """
    assert "Name" == _name_transform("name")
    assert "Kebab Case" == _name_transform("kebab-case")
    assert "123 Kebab Case" == _name_transform("123-kebab-case")
    assert "" == _name_transform("")


def test_date_transform_func():
    """
        Tests release date transform function.
    """
    assert "21.12.1998" == _release_date_transform("1998/12/21")


def test_country_name_transform():
    """
        Tests country name transform function.
    """
    assert "Sweden" == _country_name_transform("SWE")
    assert "UNKNOWN COUNTRY" == _country_name_transform("doesn't_exist")
