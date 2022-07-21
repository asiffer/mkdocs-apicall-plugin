from mkdocs_apicall_plugin.abstract import APICall, HttpMethod
from mkdocs_apicall_plugin.main import import_languages


def test_all_plugins():
    import_languages()

    kwargs = {
        "url": "http://example.com",
        "method": HttpMethod.GET,
        "headers": {
            "Authorization": "Bearer t0k3n",
            "Content-Type": "application/json",
        },
        "body": "{'a': 7}",
    }
    for Call in APICall.__subclasses__():
        print(Call(**kwargs).create_tab())
