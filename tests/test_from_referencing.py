import logging
from typing import TYPE_CHECKING

from referencing import Registry, Resource

if TYPE_CHECKING:
    from referencing.typing import Resolved, Resolver

import json
import pathlib

# def traverse(resolved: Resolved):
#     contents = resolved.contents
#     resolver = resolved.resolver

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG)
log = logging.getLogger("testing")


def resolve(resource: Resource, registry: Registry):
    log.debug(registry)
    registry.crawl()
    log.debug(registry)
    for r in resource.subresources():
        log.debug(r)
    return (resource, registry)


def main():
    resources: list[Resource] = []
    for file in pathlib.Path("tests/").glob("relative*.json"):
        with open(file) as f:
            data = json.load(f)
        schema = Resource.from_contents(data)
        resources.append(schema)
    registry = resources @ Registry()
    retrieved = registry.get_or_retrieve("urn:relative_reference:master")
    log.debug(retrieved)
    (resource, registry) = resolve(retrieved.value, retrieved.registry)
    logging.debug(resource)


if __name__ == "__main__":
    main()
