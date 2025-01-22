from datetime import datetime
from support.constants import target_columns


# обработка события и подготовка для добавления в БД
def process_event(event):
    dirs = [el for el in dir(event) if not el.startswith('__')]
    result = {attr: getattr(event, attr) for attr in dirs if attr in target_columns}

    # проверка форматов и их изменение, подготовка ввода в сводную таблицу
    if result['Data'] == b'':
        result['Data'] = None

    for key in ['TimeGenerated', 'TimeWritten']:
        if isinstance(result.get(key), datetime):
            result[key] = datetime.fromtimestamp(result[key].timestamp())

    if isinstance(result.get('StringInserts'), (tuple, list)):
        result['StringInserts'] = '|'.join(result['StringInserts'])
    elif result.get('StringInserts') is None:
        result['StringInserts'] = None

    return tuple(result.values())