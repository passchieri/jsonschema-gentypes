import json
import logging
import pathlib

from referencing import Registry, Resource

from jsonschema_gentypes import configuration
from jsonschema_gentypes.cli import process_config

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG)


def main():
    config: configuration.Configuration = {
        "python_version": "3.8",
        "generate": [
            {
                "source": "test/schemas/relative_reference_master.json",
                "destination": "test_output/types.py",
            }
        ],
    }
    files = [str(file) for file in pathlib.Path("test/schemas/").glob("relative*.json")]
    process_config(config, files)


def referencing_main():
    resources: list[Resource] = []
    for file in pathlib.Path("test/schemas/").glob("relative*.json"):
        with open(file) as f:
            data = json.load(f)
        schema = Resource.from_contents(data)
        resources.append(schema)
    registry = resources @ Registry()
    resolver = registry.resolver()
    resolved = resolver.lookup("urn:relativereference:master")
    logging.info(resolved.contents)


main()
