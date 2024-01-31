import sys

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

from typing import Any, Tuple, Union

from typing_extensions import Protocol, runtime_checkable

from lilya._internal._connection import Connection
from lilya.types import ASGIApp, Receive, Scope, Send

P = ParamSpec("P")


@runtime_checkable
class AuthenticationProtocol(Protocol[P]):  # pragma: no cover
    __slots__ = ("app",)

    def __init__(self, app: ASGIApp, *args: P.args, **kwargs: P.kwargs): ...

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None: ...

    async def authenticate(self, conn: Connection) -> Union[Tuple[Any, ...], None]: ...
