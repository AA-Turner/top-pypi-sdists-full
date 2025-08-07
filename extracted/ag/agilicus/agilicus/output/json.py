import datetime
import json


# Allows us to customize the output based on the context.
def jsonify(ctx, entry):
    return entry


def json_output_default(o):
    try:
        # The classes in our API do not serialise.
        # attempt a to_dict. If that passes, use it,
        # else continue to check for date
        o = o.to_dict()
        return o
    except AttributeError:
        pass
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return None


def convert_to_json(ctx, entry, indent=2):
    return json.dumps(
        jsonify(ctx, entry), sort_keys=True, indent=indent, default=json_output_default
    )


def output_json(ctx, entry, indent=2):
    print(convert_to_json(ctx, entry, indent=indent))


def output_json_to_file(ctx, doc, outfile):
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, default=json_output_default, indent=4)
