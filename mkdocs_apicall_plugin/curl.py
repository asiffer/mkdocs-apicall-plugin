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

        cmd = ["curl"]
        opts = self._language_config.get("options", [])
        if isinstance(opts, str):
            opts = [opts]
        # append options
        cmd += opts

        out = cmd + ["-X", self._method] + headers + data + [f"'{self._url}'"]
        test_out = " ".join(out)
        if len(test_out) < self._max_line_length:
            return test_out

        # otherwise multiline
        headers = [f"\\\n{self.indent}" + h for h in headers]
        data = [f"\\\n{self.indent}" + d for d in data]
        return " ".join(
            cmd
            + ["-X", self._method]
            + headers
            + data
            + [f"\\\n{self.indent}'{self._url}'"]
        )
