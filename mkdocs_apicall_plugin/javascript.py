import json
from typing import Any, Dict

from .abstract import APICall


class JavascriptAPICall(APICall):
    name: str = "javascript"
    icon: str = ":material-language-javascript:"
    lang: str = "js"
    indent: str = "  "

    def render_code(self) -> str:
        fetch_init: Dict[str, Any] = {"method": self._method}
        if len(self._headers) > 0:
            fetch_init["headers"] = self._headers
        if len(self._body) > 0:
            fetch_init["body"] = f"JSON.stringify({self._body})"

        out = (
            f"fetch('{self._url}', "
            + json.dumps(fetch_init, indent=None)
            .replace(r"\"", '"')
            .replace('"JSON.stringify', "JSON.stringify")
            .replace('})"', "})")
            + ");"
        )
        if len(out) < self._max_line_length:
            return out

        out = (
            f"fetch('{self._url}', "
            + json.dumps(fetch_init, indent=self.indent)
            .replace(r"\"", '"')
            .replace('"JSON.stringify', "JSON.stringify")
            .replace('})"', "})")
            + ");"
        )
        return out
