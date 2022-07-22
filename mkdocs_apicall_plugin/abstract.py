from abc import ABC
from enum import Enum
from typing import Any, Dict


class HttpMethod(str, Enum):
    """Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods"""

    # The GET method requests a representation of the specified resource.
    # Requests using GET should only retrieve data.
    GET = "GET"
    # The HEAD method asks for a response identical to a GET request,
    # but without the response body.
    HEAD = "HEAD"
    # The POST method submits an entity to the specified resource, often
    # causing a change in state or side effects on the server.
    POST = "POST"
    # The PUT method replaces all current representations of the target
    # resource with the request payload.
    PUT = "PUT"
    # The DELETE method deletes the specified resource.
    DELETE = "DELETE"
    # The CONNECT method establishes a tunnel to the server identified
    # by the target resource.
    CONNECT = "CONNECT"
    # The OPTIONS method describes the communication options for the
    # target resource.
    OPTIONS = "OPTIONS"
    # The TRACE method performs a message loop-back test along the
    # path to the target resource.
    TRACE = "TRACE"
    # The PATCH method applies partial modifications to a resource.
    PATCH = "PATCH"


class APICall(ABC):
    name: str = "undefined"
    icon: str = ""
    lang: str = ""
    indent: str = " " * 4

    _max_line_length: int = 90

    def __init__(
        self,
        url: str,
        method: HttpMethod = HttpMethod("GET"),
        headers: Dict[str, Any] = {},
        body: str = "",
        plugin_config: dict = {},
    ):
        self._method = method
        self._url = url
        self._headers = headers
        self._body = body

        # general config
        self._max_line_length = plugin_config.get("line_length", 90)
        self._print_icon = plugin_config.get("icons", False)
        # language specific config
        self._language_config = self.extract_config(plugin_config)

    def extract_config(self, plugin_config: dict) -> dict:
        for lang in plugin_config["languages"]:
            if isinstance(lang, dict):
                k: str = next(iter(lang.keys()))
                if k == self.name:
                    return lang[k]
            elif lang == self.name:
                # it means this is not necessary to
                # keep on
                break
        return {}

    def render_code(self) -> str:
        raise NotImplementedError("It must be implemented")

    def create_tab(self) -> str:
        header = self.name
        if self._print_icon and len(self.icon) > 0:
            header = f"{self.icon} {self.name}"

        code = "\n    ".join(self.render_code().splitlines())
        return f"""
=== "{header}"

    ```{self.lang}
    {code}
    ```
"""
