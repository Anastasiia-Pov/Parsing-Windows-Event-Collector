# Parsing-Windows-Event-Collector

### Запуск Clickhouse локально
1. Поднимаем docker-контейнер:
`docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server
`
2. Проверяем по http://localhost:8123, что приходит ответ Ок.


### Структура проекта
```
Parsing-Windows-Event-Collector          # родительская директория приложения/у вас может быть другое название
├─ DB/                                   # директория для работы с БД                           
│  ├─ __init__.py                           
│  ├─ db_connetion.py                    # подключение к ClickHouse
├─ scripts/                              # директория скриптов для работы с журналом событий                           
│  ├─ __init__.py                           
│  ├─ live_listener.py                   # скрипт онлайн парсера
│  ├─ parser_script_by_day.py            # парсер по указанной дате
├─ support/                              # директория скриптов для работы с журналом событий                           
│  │  ├─ __init__.py                        
│  │  ├─ constants.py                    # константы
│  │  ├─ service.py                      # вспомогательные функции
├─ config.py                             # переменные env
