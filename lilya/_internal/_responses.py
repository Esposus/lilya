from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Union

from lilya._internal._exception_handlers import wrap_app_handling_exceptions
from lilya.compat import is_async_callable
from lilya.concurrency import run_in_threadpool
from lilya.enums import SignatureDefault
from lilya.requests import Request
from lilya.responses import Response
from lilya.types import ASGIApp, Receive, Scope, Send
from lilya.websockets import WebSocket

if TYPE_CHECKING:
    pass


class BaseHandler:
    """
    Utils class that
    """

    def handle_response(
        self, func: Callable[[Request], Union[Awaitable[Response], Response]]
    ) -> ASGIApp:
        """
        Decorator for creating a request-response ASGI application.

        Args:
            func (Callable): The function to be wrapped.

        Returns:
            ASGIApp: The ASGI application.
        """

        async def app(scope: Scope, receive: Receive, send: Send) -> None:
            """
            ASGI application handling request-response.

            Args:
                scope (Scope): The request scope.
                receive (Receive): The receive channel.
                send (Send): The send channel.

            Returns:
                None
            """
            request = Request(scope=scope, receive=receive, send=send)

            async def inner_app(scope: Scope, receive: Receive, send: Send) -> None:
                """
                Inner ASGI application handling request-response.

                Sometimes the handler does not need the request to be passed
                in the handler and we can avoid it by ignoring the request
                object in the arguments.

                Args:
                    scope (Scope): The request scope.
                    receive (Receive): The receive channel.
                    send (Send): The send channel.

                Returns:
                    None
                """

                signature: inspect.Signature = self.signature
                func_params: dict[str, Any] = self._extract_params_from_request(
                    request=request, signature=signature
                )
                if signature.parameters:
                    if SignatureDefault.REQUEST in signature.parameters:
                        response = await self._execute_function(func, request, **func_params)
                    else:
                        response = await self._execute_function(func, **func_params)
                else:
                    response = await self._execute_function(func, **func_params)
                await response(scope, receive, send)

            await wrap_app_handling_exceptions(inner_app, request)(scope, receive, send)

        return app

    def _extract_params_from_request(
        self, request: Request, signature: inspect.Signature
    ) -> dict[str, Any]:
        """
        Extracts parameters from the request and injects them into the function if needed.

        Args:
            request (Request): The incoming request.
            signature (inspect.Signature): The signature of the target function.

        Returns:
            Dict[str, Any]: A dictionary containing parameters extracted from the request.
        """
        return {
            param: value
            for param, value in request.path_params.items()
            if param in signature.parameters
        }

    def handle_websocket_session(self, func: Callable[[WebSocket], Awaitable[None]]) -> ASGIApp:
        """
        Decorator for creating a WebSocket session ASGI application.

        Args:
            func (Callable): The function to be wrapped.

        Returns:
            ASGIApp: The ASGI application.
        """

        async def app(scope: Scope, receive: Receive, send: Send) -> None:
            """
            ASGI application handling WebSocket session.

            Args:
                scope (Scope): The request scope.
                receive (Receive): The receive channel.
                send (Send): The send channel.

            Returns:
                None
            """
            session = WebSocket(scope=scope, receive=receive, send=send)

            async def inner_app(scope: Scope, receive: Receive, send: Send) -> None:
                """
                Inner ASGI application handling WebSocket session.

                Args:
                    scope (Scope): The request scope.
                    receive (Receive): The receive channel.
                    send (Send): The send channel.

                Returns:
                    None
                """
                await self._execute_function(func, session)

            await wrap_app_handling_exceptions(inner_app, session)(scope, receive, send)

        return app

    async def _execute_function(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Executes the given function, handling both synchronous and asynchronous functions.

        Args:
            func (Callable): The function to execute.
            args (Any): Positional arguments for the function.
            kwargs (Any): Keyword arguments for the function.

        Returns:
            Any: The result of the function execution.
        """
        if is_async_callable(func):
            return await func(*args, **kwargs)
        else:
            return await run_in_threadpool(func, *args, **kwargs)