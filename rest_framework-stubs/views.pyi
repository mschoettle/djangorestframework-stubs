from collections.abc import Callable, Mapping, Sequence
from typing import Any, NoReturn, Protocol, TypeVar

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.views.generic import View
from rest_framework.authentication import BaseAuthentication
from rest_framework.metadata import BaseMetadata
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import BaseParser
from rest_framework.permissions import _PermissionClass, _SupportsHasPermission
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas.inspectors import ViewInspector
from rest_framework.settings import APISettings
from rest_framework.throttling import BaseThrottle
from rest_framework.versioning import BaseVersioning

def get_view_name(view: APIView) -> str: ...
def get_view_description(view: APIView, html: bool = ...) -> str: ...
def set_rollback() -> None: ...
def exception_handler(exc: Exception, context) -> Response | None: ...

_View = TypeVar("_View", bound=Callable[..., HttpResponseBase])

class AsView(Protocol[_View]):
    cls: type[APIView]
    view_class: type[APIView]
    view_initkwargs: Mapping[str, Any]
    csrf_exempt: bool
    __call__: _View

# Call signature for view function that's returned by as_view()
class GenericView(Protocol):
    def __call__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response: ...

class APIView(View):
    args: Any
    authentication_classes: Sequence[type[BaseAuthentication]]
    content_negotiation_class: type[BaseContentNegotiation]
    format_kwarg: Any
    headers: dict[str, str]
    kwargs: Any
    metadata_class: str | BaseMetadata | None
    parser_classes: Sequence[type[BaseParser]]
    permission_classes: Sequence[_PermissionClass]
    renderer_classes: Sequence[type[BaseRenderer]]
    request: Request
    response: Response
    schema: ViewInspector | None
    settings: APISettings
    throttle_classes: Sequence[type[BaseThrottle]]
    versioning_class: type[BaseVersioning] | None
    @property
    def allowed_methods(self) -> list[str]: ...
    @property
    def default_response_headers(self) -> dict[str, str]: ...
    @classmethod
    def as_view(cls, **initkwargs: Any) -> AsView[GenericView]: ...
    def http_method_not_allowed(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...  # type: ignore[override]
    def permission_denied(self, request: Request, message: str | None = ..., code: str | None = ...) -> NoReturn: ...
    def throttled(self, request: Request, wait: float) -> NoReturn: ...
    def get_authenticate_header(self, request: Request) -> str: ...
    def get_parser_context(self, http_request: HttpRequest) -> dict[str, Any]: ...
    def get_renderer_context(self) -> dict[str, Any]: ...
    def get_exception_handler_context(self) -> dict[str, Any]: ...
    def get_view_name(self) -> str: ...
    def get_view_description(self, html: bool = ...) -> str: ...
    def get_format_suffix(self, **kwargs: Any) -> str | None: ...
    def get_renderers(self) -> list[BaseRenderer]: ...
    def get_parsers(self) -> list[BaseParser]: ...
    def get_authenticators(self) -> list[BaseAuthentication]: ...
    def get_permissions(self) -> Sequence[_SupportsHasPermission]: ...
    def get_throttles(self) -> list[BaseThrottle]: ...
    def get_content_negotiator(self) -> BaseContentNegotiation: ...
    def get_exception_handler(self) -> Callable: ...
    def perform_content_negotiation(self, request: Request, force: bool = ...) -> tuple[BaseRenderer, str]: ...
    def perform_authentication(self, request: Request) -> None: ...
    def check_permissions(self, request: Request) -> None: ...
    def check_object_permissions(self, request: Request, obj: Any) -> None: ...
    def check_throttles(self, request: Request) -> None: ...
    def determine_version(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> tuple[str | None, BaseVersioning | None]: ...
    def initialize_request(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Request: ...
    def initial(self, request: Request, *args: Any, **kwargs: Any) -> None: ...
    def finalize_response(self, request: Request, response: Response, *args: Any, **kwargs: Any) -> Response: ...
    def handle_exception(self, exc: Exception) -> Response: ...
    def raise_uncaught_exception(self, exc: Exception) -> NoReturn: ...
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase: ...  # type: ignore[override]
    def options(self, request: Request, *args: Any, **kwargs: Any): ...  # type: ignore[override]
