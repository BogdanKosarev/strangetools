from unittest.mock import patch, call

import pytest

from src.strangetools.strangecollections import GWRGIDict


@pytest.fixture
def objects_data():
    return [{'some_field': 100, 'source': ['base', 'advanced']},
            {'some_field': 500, 'source': ['advanced']},
            {'source': ['base'], 'another_field': 'x'},
            {'source': 'some', 'another_field': 'y'},
            {'not_source': ['not_some'], 'another_field': 'z'}]


@pytest.fixture
def mock_choices():
    with patch('random.choices', side_effect=['key_1', 'key_2', 'key_3', 'key_4', 'key_5']) as mock_result:
        yield mock_result


def test_creation_with_plane_data(mock_choices):
    gwrgi_dict = GWRGIDict(['value_1', 'value_2', 'value_3'], None)

    assert len(gwrgi_dict._data) == 3
    assert len(gwrgi_dict._groups) == 0

    assert gwrgi_dict.get('key_1') == 'value_1'
    assert gwrgi_dict.get('key_2') == 'value_2'
    assert gwrgi_dict.get('key_3') == 'value_3'
    mock_choices.assert_has_calls([call('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6)] * 3)


def test_creation_with_objects_no_groups(mock_choices, objects_data):
    gwrgi_dict = GWRGIDict(objects_data, None)

    assert len(gwrgi_dict._data) == 5
    assert len(gwrgi_dict._groups) == 0

    assert gwrgi_dict.get('key_1')['some_field'] == 100
    assert gwrgi_dict.get('key_2')['some_field'] == 500
    assert gwrgi_dict.get('key_3')['another_field'] == 'x'
    assert gwrgi_dict.get('key_4')['another_field'] == 'y'
    assert gwrgi_dict.get('key_5')['another_field'] == 'z'
    mock_choices.assert_has_calls([call('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6)] * 3)

def test_creation_with_objects_with_groups(mock_choices, objects_data):
    gwrgi_dict = GWRGIDict(objects_data, 'source')

    assert len(gwrgi_dict._data) == 5
    assert len(gwrgi_dict._groups) == 3
    assert len(gwrgi_dict._groups['base']) == 2
    assert len(gwrgi_dict._groups['advanced']) == 2
    assert len(gwrgi_dict._groups['some']) == 1

    assert gwrgi_dict.get('key_1')['some_field'] == 100
    assert gwrgi_dict.get('key_2')['some_field'] == 500
    assert gwrgi_dict.get('key_3')['another_field'] == 'x'
    assert gwrgi_dict.get('key_4')['another_field'] == 'y'
    assert gwrgi_dict.get('key_5')['another_field'] == 'z'
    mock_choices.assert_has_calls([call('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6)] * 3)

@patch('random.choice')
def test_get_random(mock_choice, mock_choices, objects_data):
    mock_choice.return_value = 'key_4'

    gwrgi_dict = GWRGIDict(objects_data, 'source')
    assert gwrgi_dict.get_random()['another_field'] == 'y'

@patch('random.choice')
def test_get_random_from_group(mock_choice, mock_choices, objects_data):
    mock_choice.return_value = 'key_4'

    gwrgi_dict = GWRGIDict(objects_data, 'source')
    assert gwrgi_dict.get_random_from_group('some')['another_field'] == 'y'

