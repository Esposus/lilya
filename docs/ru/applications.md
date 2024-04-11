# Приложения

Lilya предоставляет класс под названием `Lilya`, который объединяет в себе
всю функциональность приложения.

```python
from lilya.apps import Lilya
```

There are many ways of creating a Lilya application but:
Существует множество способов создания приложения, например:

=== "В двух словах"

    ```python
    {!> ../docs_src/applications/nutshell.py !}
    ```

=== "с использованием Include"

    ```python
    {!> ../docs_src/applications/with_include.py!}
    ```

## Тестирование с помощью curl

```shell
$ curl -X GET http://localhost:8000/user/lilya
```

## Создание экземпляра приложения

Существует несколько способов создания экземпляра приложения. Использование [настроек](./settings.md) делает этот процесс проще.

**Параметры**:

* **debug** - Булево значение, указывающее, должна ли отладочная трассировка возвращать ошибки.
В целом, режим отладки очень полезен для разработки.
* **settings_module** - Экземпляр [settings](./settings.md) или определение класса из которого будут считываться значения настроек.
* **routes** - Список маршрутов для обслуживания входящий HTTP и WebSocket запросов.
Список [Path](./routing.md#path), [WebSocketPath](./routing.md#websocketpath), [Include](./routing.md#include) и [Host](./routing.md#host) запросов (HTTP and Websockets).
* **permissions** - Список [разрешений](./permissions.md) для обслуживания входящих запросов приложения (HTTP and Websockets).
* **middleware** - Список [промежуточных обработчиков](./middleware.md), которые будут запускаться при выполнении каждого запроса. Промежуточные обработчики могут быть подклассом [MiddlewareProtocol](./middleware.md#protocol).
* **exception handlers** - Словарь [exception types](./exceptions.md) (или пользовательских исключений) и соответствующих им функций обработчиков на верхнем уровне приложения. Вызываемые объекты (callables) обработчиков исключений должны иметь вид `handler(request, exc) -> response` и могут быть как стандартными, так и асинхронными функциями.
* **on_shutdown** - Список вызываемых объектов запускаемых при завершении работы приложения. Они не принимают никаких аргументов и могут быть как стандартными, так и асинхронными функциями.
* **on_startup** - Список вызываемых объектов запускаемых при начале работы приложения. Они не принимают никаких аргументов и могут быть как стандартными, так и асинхронными функциями.
* **lifepan** - Функция контекста работы приложения - это более новый стиль, который заменяет обработчики on_startup / on_shutdown. Используйте один или другой подход, но не оба.
* **include_in_schema** - Флаг с булевым значением, указывающий, следует ли включать схему или нет. Это может быть полезным, если вы отказываетесь от всего [включенного](./routing.md#include) приложения Lilya в пользу нового. Флаг указывает на то, что все пути должны считаться устаревшими.
* **redirect_slashes** - Флаг для включения/выключения косых черт ("/") перенаправления для обработчиков. По умолчанию он включен.

## Настройки приложения

Настройки - еще один способ управления параметрами передаваемых
[Объекту Lilya при инициализации](#instantiating-the-application). Подробнее и о том, как использовать их для настройки вашего приложения, можно узнать в [разделе настроек](./settings.md).

Для доступа к настройкам приложения есть несколько способов:

=== "Внутри запроса (request) приложения"

    ```python hl_lines="6"
    {!> ../docs_src/applications/settings/within_app_request.py!}
    ```

=== "Из глобальных настроек"

    ```python hl_lines="1 6"
    {!> ../docs_src/applications/settings/global_settings.py!}
    ```

## Состояние (State) and экземпляр приложения

Вы можете хранить произвольное дополнительное состояние в экземпляре приложения, используя атрибут `state`.

Пример:

```python hl_lines="6"
{!> ../docs_src/applications/app_state.py !}
```

## Доступ к экземпляру приложения

Экземпляр приложения **всегда** доступен через `request` или через `context`.

**Пример**

```python
from lilya.apps import Lilya
from lilya.requests import Request
from lilya.context import Context
from lilya.routing import Path


# Для запроса
def home_request(request: Request):
    app = request.app
    return {"message": "Welcome home"}


# Для контекста
def home_context(context: Context):
    app = context.app
    return {"message": "Welcome home"}


app = Lilya(routes=[
        Path("/request", home_request),
        Path("/context", home_context),
    ]
)
```
