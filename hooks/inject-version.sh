#!/bin/sh

VERSION=$(poetry version -s)
echo '__version__ = "'"${VERSION}"'"' > mkdocs_apicall_plugin/__init__.py
exit 0
