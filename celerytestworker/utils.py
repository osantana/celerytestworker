# coding: utf-8


from importlib import import_module


def get_application(dotted_path):
    try:
        module_path, identifier = dotted_path.rsplit('.', 1)
        module = import_module(module_path)
        application = getattr(module, identifier)
    except (ValueError, AttributeError):
        raise ImportError("Invalid reference {!r}".format(dotted_path))

    return application
