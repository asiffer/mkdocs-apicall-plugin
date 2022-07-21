from .abstract import APICall


class CurlAPICall(APICall):
    name: str = "curl"
    icon: str = ":material-web:"
    lang: str = "shell"
    indent: str = " " * 5

    def render_code(self) -> str:
        # try to inline everything
        headers = [f"-H '{k}: {v}'" for k, v in self._headers.items()]
        data = [f"-d '{self._body}'"] if len(self._body) > 0 else []
        out = (
            ["curl", "-X", self._method] + headers + data + [f"'{self._url}'"]
        )
        test_out = " ".join(out)
        if len(test_out) < self._max_line_length:
            return test_out

        # otherwise multiline
        headers = [f"\\ \n{self.indent}" + h for h in headers]
        data = [f"\\ \n{self.indent}" + d for d in data]
        return " ".join(
            ["curl", "-X", self._method] + headers + data + [f"'{self._url}'"]
        )
