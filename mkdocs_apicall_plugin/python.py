import black
from black.mode import Mode

from .abstract import APICall


class PythonAPICall(APICall):
    name: str = "python"
    icon: str = ":material-language-python:"
    lang: str = "python"

    def render_code(self) -> str:
        out = f'"{self._url}"'
        if len(self._headers) > 0:
            out += (
                ", headers={"
                + ", ".join(
                    f'"{key}": "{value}"'
                    for key, value in self._headers.items()
                )
                + "}"
            )

        if len(self._body) > 0:
            out += f", data={self._body}"

        return black.format_str(
            f"""
import requests

r = requests.{self._method.lower()}({out})
""",
            mode=Mode(line_length=self._max_line_length),
        )
