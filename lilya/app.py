from __future__ import annotations

from typing import (
    Any,
    AsyncContextManager,
    Awaitable,
    Callable,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Annotated, Doc

from lilya._utils import is_class_and_subclass
from lilya.conf.exceptions import FieldException
from lilya.conf.global_settings import Settings
from lilya.types import ApplicationType, ASGIApp, ExceptionHandler, Lifespan, Receive, Scope, Send


class Lilya:
    """
    Creates an application instance.

    * **debug** - Boolean indicating if debug tracebacks should be returned on errors.
    * **routes** - A list of routes to serve incoming HTTP and WebSocket requests.
    * **middleware** - A list of middleware to run for every request.
    * **exception_handlers** - A mapping of either integer status codes,
    * **on_startup** - A list of callables to run on application startup.
    Startup handler callables do not take any arguments, and may be be either
    standard functions, or async functions.
    * **on_shutdown** - A list of callables to run on application shutdown.
    Shutdown handler callables do not take any arguments, and may be be either
    standard functions, or async functions.
    * **lifespan** - A lifespan context function, which can be used to perform
    startup and shutdown tasks. This is a newer style that replaces the
    `on_startup` and `on_shutdown` handlers. Use one or the other, not both.
    * **permissions** - A list of permissions to run on the top level of a
    lilya instance.
    * include_in_schema** - Boolean flag indicating if the routes of the instance
    should be included in the OpenAPI schema.
    """

    def __init__(
        self,
        debug: bool = False,
        routes: Union[Sequence[Any], None] = None,
        middleware: Union[Sequence[Any], None] = None,
        exception_handlers: Union[Mapping[Any, ExceptionHandler], None] = None,
        permissions: Union[Sequence[Any], None] = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Optional[Lifespan["ApplicationType"]] = None,
        settings_config: Annotated[
            Optional[Settings],
            Doc(
                """
                Alternative settings parameter. This parameter is an alternative to
                `LILYA_SETTINGS_MODULE` way of loading your settings into an Esmerald application.

                When the `settings_config` is provided, it will make sure it takes priority over
                any other settings provided for the instance.


                !!! Tip
                    The settings module can be very useful if you want to have, for example, a
                    [ChildEsmerald](https://esmerald.dev/routing/router/?h=childe#child-esmerald-application) that needs completely different settings
                    from the main app.

                    Example: A `ChildEsmerald` that takes care of the authentication into a cloud
                    provider such as AWS and handles the `boto3` module.
                """
            ),
        ] = None,
    ) -> None:
        assert lifespan is None or (
            on_startup is None and on_shutdown is None
        ), "Use either 'lifespan' or 'on_startup'/'on_shutdown', not both."

        self.settings_config = None

        if settings_config:
            if not isinstance(settings_config, Settings) and not is_class_and_subclass(
                settings_config, Settings
            ):
                raise FieldException("'settings_config' must be a subclass of Settings")
            elif isinstance(settings_config, Settings):
                self.settings_config = settings_config  # type: ignore
            elif is_class_and_subclass(settings_config, Settings):
                self.settings_config = settings_config()