import clickhouse_connect
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, INTERFACE, DB_PASSWORD

try:
    # Подключение к ClickHouse
    client = clickhouse_connect.get_client(host=DB_HOST,
                                           port=DB_PORT,
                                           username=DB_USER,
                                           password=DB_PASSWORD or '',
                                           interface=INTERFACE)
    client.command(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    print(f"Database '{DB_NAME}' created or already exists.")
    # Создание таблицы
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {DB_NAME}.events (
        ClosingRecordNumber INT,
        ComputerName String,
        Data Nullable(String),
        EventCategory INT,
        EventID INT,
        EventType INT,
        RecordNumber INT,
        Reserved INT,
        ReservedFlags INT,
        Sid Nullable(String),
        SourceName String,
        StringInserts Nullable(String),
        TimeGenerated DateTime,
        TimeWritten DateTime,
    ) ENGINE = MergeTree()
    ORDER BY TimeGenerated;
    """

    # Create the table in the database
    client.command(create_table_query)
    print(f"Table 'event_logs' created or already exists in database '{DB_NAME}'.")
except Exception as e:
    print("Failed to connect to ClickHouse:", e)
