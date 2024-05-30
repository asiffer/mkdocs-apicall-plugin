#!/bin/sh

VERSION=$(poetry version -s)
echo '__version__ = "'"${VERSION}"'"' > mkdocs_apicall_plugin/__init__.py
sed -i "s/__version__ == \x22[0-9.]*\x22/__version__ == \x22${VERSION}\x22/" tests/test_mkdocs_apicall_plugin.py
exit 0
