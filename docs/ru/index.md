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

**Documentation**: [https://lilya.dev](https://lilya.dev) 📚

**Source Code**: [https://github.com/dymmond/lilya](https://github.com/dymmond/lilya)

**The official supported version is always the latest released**.

---

## Мотивация

В мире ASGI всегда полезно иметь альтернативы, и ни один инструмент не может обеспечить все потребности.
Создание Lilya вдохновлено фреймворками, которые стояли у истоков веб разработки на Python. Она представляет собой более простой, точный, быстрый и удобный в использовании набор инструментов (фреймворк) на Python, нацеленный на простоту.

Часто нет необходимости в полноценном веб-фреймворке на Python, так как это может быть излишним
для решения простых задач. Вместо этого предпочтительнее использовать простой ASGI-инструментарий, который поможет в создании готовых к продакшену, быстрых, элегантных, поддерживаемых и модульных приложений.

Именно здесь Lilya находит своё применение.

Почти без жестких зависимостей, 100% написаный на Python, полностью типизированный и готовый к использованию в продакшене.

## What does it bring?

Lilya comes bearing fruits.

* A lightweight ASGI toolkit/framework.
* Support for HTTP/WebSocket.
* Tasks (in ASGI known as background tasks).
* Lifespan events (on_startup/on_shutdown and lifespan).
* Native permission system.
* Middlewares (Compressor, CSRF, Session, CORS...).
* A native and **optional** [client](./lilya-cli.md).
* **Directive management control system** for any custom scripts to run inside the application.
* Little hard dependencies.
* Compatibility with `trio` and `asyncio`.
* Dynamic routing system with the help of the native **Include** and minimum boilerplate.
* Native settings system. No more bloated instances.

## Installation

If you want just the toolkit/framework.

```shell
$ pip install lilya
```

If you wish to use to extra functionalities such as the **shell** or **directives**
(project scaffold generation to speed up).

```shell
$ pip install lilya[cli,ipython] # for ipython shell
$ pip install lilya[cli,ptpython] # for ptpython shell
```

You can learn more about the [client](./directives/discovery.md) in the documentation.

Or if you want to install everything that will allow you to use all the resources of Lilya, such
as some specific middlewares.

```shell
$ pip install lilya[all]
```

### Additional

You would want to install an ASGI server such as [uvicorn](https://www.uvicorn.org/) or
[hypercorn](https://pgjones.gitlab.io/hypercorn/) as well.

## Quickstart

If you are familiar with other Python frameworks and toolkits, Lilya provides you with the same
feeling.

A Lilya also uses a [native settings system](./settings.md) which is something that can be extremely useful
for any application.

```python
{!> ../docs_src/quickstart/app.py !}
```

Is this simple. Although there is a lot to unwrap here. Did you notice the path `/{user}` not only
does not require a `request` to be declared and instead, receives a `user: str`?

Well, Lilya does a lot of internal magic for you. If you don't declare a `request`, that is not a
problem as it will only pass it if its there.

If you have the path parameter declared in the function handler as well, Lilya will automatically
search for the parameters declared and match them against the path parameters declared in the `Path`
and inject them for you.

Pretty cool, right? This is just scratching the surface.

## Definitions

Lilya can be considered a framework or a toolkit and the reasoning for it its because each component
such as middlewares, permissions, Path, Router... can be seen as an independent ASGI application.

In other words, you can build a [middleware](./middleware.md) or a [permission](./permissions.md) and
share those with any other existing ASGI framework out there, meaning, you could design a Lilya
application, middlewares, permissions and any other component and re-use them in [Esmerald][esmerald]
or [FastAPI][fastapi] or any other, really.

**Lilya is not a full-fledge framework like [Esmerald][esmerald] or [FastAPI][fastapi], instead**
**its a lightweight toolkit/framework that can be used to build those as well as working on its own.**

**Example**

```python
{!> ../docs_src/quickstart/example.py !}
```

## Run the application

To run the application from the example.

```shell
$ uvicorn myapp:app
INFO:     Started server process [140552]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

[esmerald]: https://lilya.dev/esmerald
[fastapi]: https://fastapi.tiangolo.com
