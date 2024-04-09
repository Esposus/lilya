---
hide:
  - navigation
---

# Lilya

<p align="center">
  <a href="https://lilya.dev"><img src="https://res.cloudinary.com/dymmond/image/upload/v1707501404/lilya/logo_quiotd.png" alt='Lilya'></a>
</p>

<p align="center">
    <em>🚀 Yet another ASGI toolkit that delivers. 🚀</em>
</p>

<p align="center">
<a href="https://github.com/dymmond/lilya/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/dymmond/lilya/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/lilya" target="_blank">
    <img src="https://img.shields.io/pypi/v/lilya?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/lilya" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/lilya.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Документация**: [https://lilya.dev](https://lilya.dev) 📚

**Исходный код**: [https://github.com/dymmond/lilya](https://github.com/dymmond/lilya)

**Официальная поддерживаемая версия всегда является последней выпущенной версией**.

---

## Мотивация

В мире ASGI всегда полезно иметь альтернативы, и ни один инструмент не может обеспечить все потребности.
Создание Lilya вдохновлено фреймворками, которые стояли у истоков веб разработки на Python. Она представляет собой более простой, точный, быстрый и удобный в использовании набор инструментов (фреймворк) на Python, нацеленный на простоту.

Часто нет необходимости в полноценном веб-фреймворке на Python, так как это может быть излишним
для решения простых задач. Вместо этого предпочтительнее использовать простой ASGI-инструментарий, который поможет в создании готовых к продакшену, быстрых, элегантных, поддерживаемых и модульных приложений.

Именно здесь Lilya находит своё применение.

Почти без жестких зависимостей, 100% написаный на Python, полностью типизированный и готовый к использованию в продакшене.

## Какие преимущества принесет Lilya?

Lilya приносит с собой целый ряд преимуществ.

* легковесный набор инструментов/фреймворк для ASGI.
* Поддержка HTTP/WebSocket.
* Задачи (в ASGI известны как фоновые задачи (background tasks)).
* События жизненого цикла - lifespan events (on_startup/on_shutdown и lifespan).
* Собственная система разрешений (permissions).
* Middlewares (Compressor, CSRF, Session, CORS...).
* Собственный и **опциональный** [клиент](./lilya-cli.md).
* **Система управления директивами** для запуска любых пользовательских скриптов внутри приложения.
* Минимальное количество жестких зависимостей.
* Совместимость с `trio` и `asyncio`.
* Динамическая система маршрутизации с использованием нативного **Include** и минимального бойлерплейта.
* Собственная система настроек. Больше никаких раздутых экземпляров.

## Установка

Если Вам нужно установить только фреймворк.

```shell
$ pip install lilya
```

Если вы хотите использовать дополнительные возможности, такие как **shell** или **directives**
(создание шаблона проекта для более быстрого старта разработки).

```shell
$ pip install lilya[cli,ipython] # для ipython shell
$ pip install lilya[cli,ptpython] # для ptpython shell
```

Подробнее о [клиенте](./directives/discovery.md) вы можете узнать в документации.

Либо вы можете установить сразу всё, чтобы использовать все возможности Lilya,
как, например, определенные middleware.

```shell
$ pip install lilya[all]
```

### Дополнительно

Вам потребуется установить ASGI сервер, например [uvicorn](https://www.uvicorn.org/) или
[hypercorn](https://pgjones.gitlab.io/hypercorn/).

## Быстрый старт

Для вас многое будет уже знакомым, если вы имеете опыт работы с фреймворками и веб-инструментами на Python.

Кроме того, Lilya использует [собственную систему настроек](./settings.md),
что может быть чрезвычайно полезно для любого приложения.

```python
{!> ../docs_src/quickstart/app.py !}
```

Просто, не правда ли? Хотя здесь есть о чем рассказать. Вы заметили, что путь `/{user}`
не только не требует объявления `request`, но и вместо этого получает `user: str`?

Lilya творит много внутренней магии для вас. Если вы не объявляете `request` это не проблема, 
так как он будет передан только в том случае, если он есть.

Если вы передали path параметр и в хэндлере, то Lilya автоматически выполнит поиск объявленных параметров, сопоставит их
с параметрами path, объявленными в `Path`, и подставит их за вас.

Круто, не так ли? И это только начало!

## Определения

Lilya можно рассматривать как фреймворк или как набор инструментов (англ. toolkit) и это объясняется тем, что каждый
компонент, такой как middlewares, permissions, Path, Router... можно рассматривать как независимые ASGI приложения.

Другими словами, вы можете создать [middleware](./middleware.md) или [permission](./permissions.md) и использовать их с 
любым другим существующим ASGI фреймворком, то есть вы действительно можете создать приложение Lilya, middlewares, permissions и 
любой другой компонент и переиспользовать их в [Esmerald][esmerald] или [FastAPI][fastapi], или с любым другим.

**Lilya не полноценный фреймворк как [Esmerald][esmerald] или [FastAPI][fastapi], а легковесный**
**набор инструментов/фреймворк, который можно использовать как для создания новых фреймворков, 
так и для самостоятельной разработки.**

**Пример**

```python
{!> ../docs_src/quickstart/example.py !}
```

## Запуск приложения

Чтобы запустить приложение из примера.

```shell
$ uvicorn myapp:app
INFO:     Started server process [140552]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

[esmerald]: https://lilya.dev/esmerald
[fastapi]: https://fastapi.tiangolo.com
