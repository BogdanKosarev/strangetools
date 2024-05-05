import random
import string


class GWRGIDict:
    """
    Grouped With Random Get immutable dictionary
    """

    _key_alphabet = string.ascii_letters + string.digits

    def __init__(self, data: list, group_key_field: str, other=(), /, **kwds):
        self._groups = dict()
        self._data = dict()

        for item in data:
            key = ''.join(random.choices(GWRGIDict._key_alphabet, k=6))
            self._data[key] = item
            if group_key_field and group_key_field in item:
                group_key_value = item[group_key_field]
                if isinstance(group_key_value, list):
                    for single_value in group_key_value:
                        self._add_to_group(single_value, key)
                else:
                    self._add_to_group(group_key_value, key)

    def _add_to_group(self, group_key, object_key):
        group_data_list = self._groups.get(group_key, list())
        group_data_list.append(object_key)
        self._groups[group_key] = group_data_list

    def get(self, key):
        return self._data[key]

    def get_random(self):
        return self._data[random.choice(self._data.keys())]

    def get_random_from_group(self, group_key: str):
        return self._data[random.choice(self._groups[group_key])]
