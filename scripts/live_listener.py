import win32event
import win32evtlog
from datetime import datetime
from config import DB_NAME
from DB.db_connection import client
from support.service import process_event

# Открываем журнал событий
hand = win32evtlog.OpenEventLog("localhost", "Security")
flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
# Создаем объект-событие
event_handle = win32event.CreateEvent(None, 0, 0, None)
# Связываем объект-событие с журналом
win32evtlog.NotifyChangeEventLog(hand, event_handle)
print("Общее кол-во событий на данный момент:", total)
print('Monitoring Windows Event Log for new events...')


# определение формата даты
date_model = '%Y-%m-%d'
# определение дня выборки (по-умолчанию указан сегодняшний день)
today_date = datetime.today().strftime(date_model)
# определение EventID
event_id = 4624

# подсчет кол-ва событий за сегодняшний день
today = 0


# Связываем объект-событие с журналом
win32evtlog.NotifyChangeEventLog(hand, event_handle)


# Последний обработанный номер записи
last_record_number = -1

# Основной цикл мониторинга
try:
    while True:
        # Ждем новых событий
        win32event.WaitForSingleObject(event_handle, win32event.INFINITE)

        # Считываем новые события
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            for event in events:
                if event.EventID == event_id and last_record_number <= event.RecordNumber:
                    # result = process_event(event)
                    print(process_event(event))
                    client.insert(f"{DB_NAME}.events", [process_event(event)])
                    last_record_number = event.RecordNumber
                
except KeyboardInterrupt:
    print("Stopped monitoring Windows Event Log.")
finally:
    win32evtlog.CloseEventLog(hand)

