import json
from typing import OrderedDict


def pretty(s):
    MAX_LEN = 80
    INDENT_SIZE = 2

    def _force_wrap(parent):
        if len(parent) < 2:
            return False
        for child in parent:
            if not isinstance(child, (tuple, list, dict)):
                return False
            if len(child) < 2:
                return False
        return True

    def _encode_list(lst, indent, cursor):
        if not lst:
            return "[]"

        if not _force_wrap(lst):
            buf = "["
            first = True
            for value in lst:
                if len(buf) > MAX_LEN:
                    break
                if first:
                    first = False
                else:
                    buf += ", "
                buf += _encode(value, indent, cursor + len(buf))
            buf += "]"

            if indent + cursor + len(buf) <= MAX_LEN:
                return buf

        indent += INDENT_SIZE
        buf = "[\n" + " " * indent
        first = True
        for value in lst:
            if first:
                first = False
            else:
                buf += ",\n" + " " * indent
            buf += _encode(value, indent, 0)
        indent -= INDENT_SIZE
        buf += "\n" + " " * indent + "]"

        return buf

    def _encode_dict(dct, indent, cursor):
        if not dct:
            return "{}"

        if not _force_wrap(dct):
            buf = "{ "
            first = True
            for key, value in dct.items():
                if len(buf) > MAX_LEN:
                    break
                if first:
                    first = False
                else:
                    buf += ", "
                if not isinstance(key, str):
                    raise ValueError("Illegal key type '" + type(key).__name__ + "'")
                buf += '"' + key + '": '
                buf += _encode(value, indent, cursor + len(buf))
            buf += " }"

            if indent + cursor + len(buf) <= MAX_LEN:
                return buf

        indent += INDENT_SIZE
        buf = "{\n" + " " * indent
        first = True
        for key, value in dct.items():
            if first:
                first = False
            else:
                buf += ",\n" + " " * indent
            if not isinstance(key, str):
                raise ValueError("Illegal key type '" + type(key).__name__ + "'")
            entry = '"' + key + '": '
            buf += entry + _encode(value, indent, len(entry))
        indent -= INDENT_SIZE
        buf += "\n" + " " * indent + "}"

        return buf

    def _encode(data, indent, cursor):
        if data is None:
            return "null"
        elif data is True:
            return "true"
        elif data is False:
            return "false"
        elif isinstance(data, int):
            return int.__repr__(data)
        elif isinstance(data, float):
            return float.__repr__(data)
        elif isinstance(data, str):
            return '"' + data + '"'
        elif isinstance(data, (list, tuple)):
            return _encode_list(data, indent, cursor)
        elif isinstance(data, dict):
            return _encode_dict(data, indent, cursor)
        else:
            raise ValueError("Illegal value type '" + type(data).__name__ + "'")

    data = json.loads(s, object_pairs_hook=OrderedDict)
    return _encode(data, 0, 0)
