import importlib
import os
from typing import List, Set, Type

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from mkdocs_apicall_plugin.abstract import APICall, HttpMethod


def import_languages():
    protected = ["abstract.py", "main.py"]
    path = os.path.dirname(__file__)
    for file in os.listdir(path):
        if file.startswith("_"):
            continue
        if not file.endswith(".py"):
            continue
        if file in protected:
            continue
        # import the language
        importlib.import_module(f"mkdocs_apicall_plugin.{file.rstrip('.py')}")


class APICallPlugin(BasePlugin):
    """
    Attributes
    ----------
    config_scheme: tuple
        A tuple of configuration validation instances.
        Each item must consist of a two item tuple in
        which the first item is the string name of the
        configuration option and the second item is an
        instance of mkdocs.config.config_options.BaseConfigOption
        or any of its subclasses.
    config: dict
        A dictionary of configuration options for the
        plugin, which is populated by the load_config
        method after configuration validation has
        completed. Use this attribute to access options
        provided by the user.
    """

    config: dict
    config_scheme = (
        (
            "languages",
            config_options.Type(
                list,
                default=[{"curl": {}}, {"python": {}}, {"javascript": {}}],
            ),
        ),
        (
            "line_length",
            config_options.Type(int, default=90),
        ),
        (
            "icons",
            config_options.Type(bool, default=False),
        ),
    )
    tags: Set[str] = {"@@@"}

    def __init__(self) -> None:
        # we need to import all the supported languages
        import_languages()
        super().__init__()

    def parse_and_transform_block(self, block: List[str]) -> str:
        request = block.pop(0)
        for tag in self.tags:
            request = request.replace(tag, "")
        request = request.strip()

        try:
            # parse the first line
            method, url, body = request.split(" ", maxsplit=2)
        except ValueError:
            # it means there is no body
            method, url = request.split(" ", maxsplit=1)
            body = ""

        # parse header
        headers = {}
        for b in block:
            # here we may have empty lines if the markdown
            # is not well formatted
            if ":" in b:
                k, v = b.split(":", maxsplit=1)
                headers[k.strip()] = v.strip()

        return "\n\n".join(
            [
                Call(
                    url=url,
                    method=HttpMethod(method),
                    headers=headers,
                    body=body,
                    plugin_config=self.config,
                ).create_tab()
                for Call in self.get_calls()
            ]
        )

    def get_languages(self) -> List[str]:
        """Return the list of the languages given in the options"""
        langs: List[str] = []
        for lang in self.config["languages"]:
            # in case of options
            if isinstance(lang, dict):
                k: str = next(iter(lang.keys()))
                langs.append(k)
            # no options
            elif isinstance(lang, str):
                langs.append(lang)
        return langs

    def get_calls(self) -> List[Type[APICall]]:
        """Return the languages APICall as desired
        by the config (in the same order)"""
        registered = [c.name for c in APICall.__subclasses__()]
        return [
            APICall.__subclasses__()[registered.index(name)]
            for name in self.get_languages()
        ]

    def on_page_markdown(
        self, markdown: str, page: Page, config: dict, files: list
    ) -> str:

        is_inside_code_block = False
        lines = []
        md_lines = markdown.splitlines()
        nb_lines = len(md_lines)
        i = 0
        while i < nb_lines:
            line = md_lines[i]

            # check code block ===============================================
            if line.startswith("```"):
                if len(line) <= 3:
                    # end of block
                    is_inside_code_block = False
                else:
                    is_inside_code_block = True
            # ================================================================

            # ignore some lines ==============================================
            # do not treat lines that do not start with tag
            # and lines that are in code block
            if (not any(line.startswith(tag) for tag in self.tags)) or (
                is_inside_code_block
            ):
                lines.append(line)
                i += 1
                continue
            # ================================================================

            # Parse block ====================================================
            # here it means that we have reach a tag
            # so we must parse the block
            block = [line]
            i += 1
            while i < nb_lines and md_lines[i].startswith(" "):
                block.append(md_lines[i])
                i += 1

            for b in self.parse_and_transform_block(block).splitlines():
                lines.append(b)

            block.clear()
            # ================================================================

        return "\n".join(lines)
