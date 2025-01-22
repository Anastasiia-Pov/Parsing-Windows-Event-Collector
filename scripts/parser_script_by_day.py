import win32evtlog
from datetime import datetime
from config import DB_NAME
from DB.db_connection import client
from support.service import process_event

# Открываем журнал событий
hand = win32evtlog.OpenEventLog("localhost", "Security")
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
print("Общее кол-во событий на данный момент:", total)


# определение формата даты
date_model = '%Y-%m-%d'
# определение дня выборки (по-умолчанию указан сегодняшний день)
today_date = datetime.today().strftime(date_model)
# определение EventID
event_id = 4624

# подсчет кол-ва событий за сегодняшний день
today = 0

rows_to_insert = []
# получение событий за сегодняшний день
while True:
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    if events:

        for event in events:
            event_date = event.TimeWritten.strftime(date_model)
            if event.EventID == event_id and event_date == today_date:
                today += 1
                rows_to_insert.append(process_event(event))

        if rows_to_insert:
            client.insert(f"{DB_NAME}.events", rows_to_insert)
            # print(f"Inserted batch: {rows_to_insert}")
            rows_to_insert.clear()

    else: break

print(f"Данные с EventID {event_id} за {today_date} успешно добавлены\nОбщее кол-во событий {event_id} за {today_date}: {today}")
