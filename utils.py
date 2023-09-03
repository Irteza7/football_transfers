import brotli
import json


def get_decoded_data(content, headers):
    if headers.get('Content-Encoding') == 'br':
        try:
            decoded_content = brotli.decompress(content)
            return json.loads(decoded_content.decode('utf-8'))
        except brotli.error:
            return json.loads(content.decode('utf-8'))
    else:
        return json.loads(content.decode('utf-8'))



def get_fields(data, parent_key='', sep='.'):
    fields = []
    if isinstance(data, dict):
        for k, v in data.items():
            current_key = f"{parent_key}{sep}{k}" if parent_key else k
            fields.append(current_key)
            if isinstance(v, dict):
                fields.extend(get_fields(v, current_key, sep=sep))
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                fields.extend(get_fields(v[0], current_key, sep=sep))
    return fields



def extract_values(data, fields):
    records_list = data.get('records', [])
    
    # Placeholder for the extracted data for all records
    all_extracted_data = []
    
    for record in records_list:
        extracted_data = {}
        for field in fields:
            keys = field.split('.')
            value = record  
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key, None)
                else:
                    value = None
                    break
            extracted_data[field] = value
        all_extracted_data.append(extracted_data)

    return all_extracted_data




# Updated desired_fields list without 'records.' prefix
desired_fields = [
    'player_name',
    'country_name',
    'country_code',
    'age',
    'position_name',
    'position_short_name',
    'club_from_name',
    'club_to_name',
    'amount',
    'free',
    'disclosed',
    'type_id',
    'date_transfer',
    'price_tag.price',
    'price_tag.value',
    'price_tag.type'
]
