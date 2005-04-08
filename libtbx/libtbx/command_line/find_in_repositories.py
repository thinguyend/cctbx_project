import libtbx.load_env
from libtbx.str_utils import show_string
from libtbx.utils import Sorry
import sys, os

def run(args, this_command="libtbx.find_in_repositories"):
  if (len(args) != 1):
    raise Sorry("usage: %s name" % this_command)
  name = args[0]
  result = libtbx.env.find_in_repositories(
    relative_path=name, test=os.path.exists)
  if (result is None):
    raise Sorry("%s: cannot locate %s" % (this_command, show_string(name)))
  print result

if (__name__ == "__main__"):
  run(sys.argv[1:])
