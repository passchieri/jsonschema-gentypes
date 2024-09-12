import json

import jsonschema_gentypes.api_draft_2020_12
import jsonschema_gentypes.resolver
from jsonschema_gentypes.api import Type


def get_types(schema) -> Type:
    files = ["tests/relative_reference_master.json", "tests/relative_reference_child.json"]
    resolver = jsonschema_gentypes.resolver.RefResolver("https://example.com/fake", schema, files=files)
    api = jsonschema_gentypes.api_draft_2020_12.APIv202012(resolver)
    return api.get_type(schema, "Base")


def test_relative_references():
    with open("tests/relative_reference_master.json") as schema_file:
        data = json.load(schema_file)
    type_ = get_types(data)

    assert (
        "\n".join([d.rstrip() for d in type_.definition(None)])
        == '''

class Ref1(TypedDict, total=False):
    """ Ref1. """

    data: "Ref2"
    """ Ref2. """

    children: List["Ref1"]'''
    )
