# import django deps
from django.utils.decorators import method_decorator


# permissions decorator
def permissions_decorator():
    """
        This is a class level decorator that is able to dynamically apply
        decorators specified in the ``PYBB_CLIENT_FORUMS`` setting on to
        the passed classes ``dispatch`` method.
    """
    def dec(cls):
        orig_dispatch = cls.dispatch

        def _dispatch(self, request, *args, **kwargs):
            """
                Grab relevant decorators from the request, convert them
                into method decorators using django's ``method_decorator``
                functionality. Finally apply the decorators in reverse
                order (decorators are applied inside out) to the new dispatch
                view
            """
            new_dispatch = orig_dispatch
            if request.pybb_permission_decorators is not None:
                for dec in reversed(
                        request.pybb_permission_decorators.decorators):
                    new_dispatch = method_decorator(dec())(new_dispatch)
            return new_dispatch(self, request, *args, **kwargs)
        cls.dispatch = _dispatch
        return cls
    return dec
