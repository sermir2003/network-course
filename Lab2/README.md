# Определитель MTU

## Использование

Для сборки образа

```bash
docker build -t mtu-discover .
```

Для определения MTU

```bash
docker run -t mtu-discover [OPTIONS] TARGET
```

Где `TARGET` — это IPv4, IPv6 или Hostname, а опции из списка

```console
--lower INTEGER RANGE       The lower limit of the search
                            [0<=x<=1000000000]
--upper INTEGER RANGE       The upper limit of the search
                            [0<=x<=1000000000]
-v, --verbose               Display detailed information
-c, --count INTEGER RANGE   The count of pings per test  [0<=x<=100]
-i, --interval FLOAT RANGE  The interval between pings within a test
                            [0<=x<=5]
-W, --timeout FLOAT RANGE   Ping timeout  [0<=x<=5]
--help                      Show help message and exit.
```

Скрипт выполняет бинарный поиск MTU, в каждом тесте посылая несколько icmp-ping запросов.

## Оценивание

1. Соответствие аргумента типу проверяется библиотекой click
1. Соответствие аргумента допустимому диапазону проверяется библиотекой click
1. Доступность адреса назначения проверяется
1. Исключения отлавливаются
1. Если icmp заблокирован, скрипт действительно не работает
1. Скрипт платформонезависим
