import sys
import inspect

def call_function_get_frame(func, *args, **kwargs):

  frame = None
  trace = sys.gettrace()
  def snatch_locals(_frame, name, arg):
    nonlocal frame
    if frame is None and name == 'call':
      frame = _frame
      sys.settrace(trace)
    return trace
  sys.settrace(snatch_locals)
  try:
    print(kwargs)
    result = func(*args, **kwargs)
  finally:
    sys.settrace(trace)
  return frame, result

import types

def namespace_decorator(func):
  frame, result = call_function_get_frame(func)
  try:
    module = types.ModuleType(func.__name__)
    module.__dict__.update(frame.f_locals)
    return module
  finally:
    del frame


if __name__ != "__main__":
    import atexit
    import __main__

    def on_exit():
        
        kwargs = { key: value for key, value in vars(namespace_decorator(__main__.setup)).items() if key[0] != "_"}

        print(kwargs)

        print(inspect.getargspec(__main__.loop))

        for x in range(5):
            namespace_decorator(__main__.loop, **kwargs)


    atexit.register(on_exit)
else:
    print("\nNotice! Please run this by importing the module, inside tank code")