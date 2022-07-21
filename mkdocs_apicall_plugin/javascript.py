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

        # headers = [f"'{k}': '{v}'" for k, v in self._headers.items()]
        # data = [{self._body}] if len(self._body) > 0 else []

        # out = f"fetch('{self._url}'"
        # options = [f"method: {self._method}"]
        # if len(headers) > 0:
        #     options += [f"headers: {{{', '.join(headers)}}}"]
        # if len(data) > 0:
        #     options += [f"body: {data[0]}"]

        # test_out = out + ", {" + ", ".join(options) + "});"
        # if len(test_out) < self._max_line_length:
        #     return test_out

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
        # multiline 1
        # out = [f"fetch('{self._url}', {{"]
        # options = [f"{self.indent}{o},\n" for o in options]
        # out += options + ["});"]

        # for o in options:
        #     if le

        # # blob = f"method: '{self._method}'"
        # if len(self._headers) > 0:
        #     blob = f"\n{self.indent}{blob}"
        #     blob += f",\n{self.indent}headers: {{\n"
        #     blob += (
        #         ",\n".join(
        #             f"{self.indent * 2}'{key}': '{value}'"
        #             for key, value in self._headers.items()
        #         )
        #         + f"\n{self.indent}}}"
        #     )

        # if len(self._body) > 0:
        #     blob += f",\n{self.indent}body: JSON.stringify({self._body})"

        # return f"""fetch('{self._url}', {{ {blob} }});"""


"""
method: '{method}',{headers}
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({a: 1, b: 'Textual content'})
"""
