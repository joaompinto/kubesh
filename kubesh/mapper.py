def find_item(root_item, field_spec, keys_only=False):
    if field_spec is None:
        return root_item.to_dict()
    tokens = field_spec.split(".")
    cursor = root_item
    for tokenName in tokens:
        if tokenName[0] == "[":
            assert isinstance(cursor, list)
            tokenName = tokenName.strip("[]]")
            search_key, search_value = tokenName.split("=")
            match_item = [x for x in cursor if getattr(x, search_key) == search_value]
            if match_item:
                cursor = match_item[0]
            else:
                return None
        else:
            cursor = getattr(cursor, tokenName)
    if not isinstance(cursor, (str, int, float, tuple, list)):
        return cursor.to_dict()
    return cursor


def table_from_list(data, fields):
    input_data = data.items
    field_label_list = []
    field_spec_list = []
    for field_spec in fields:
        label, spec = list(field_spec.items())[0]
        field_label_list.append(label)
        field_spec_list.append(spec)
    response_data = [field_label_list]
    for list_item in input_data:
        row = []
        for field_spec in field_spec_list:
            value = find_item(list_item, field_spec)
            row.append(value)
        response_data.append(row)
    return response_data
