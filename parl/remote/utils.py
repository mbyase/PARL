#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ['load_remote_class']


def simplify_code(code, end_of_file):
    """
  @parl.remote_actor has to use this function to simplify the code.
  To create a remote object, PARL has to import the module that contains the decorated class.
  It may run some unnecessary code when importing the module, and this is why we use this function
  to simplify the code.

  For example.
  @parl.remote_actor
  class A(object):
    def add(self, a, b):
    return a + b
  def data_process():
    XXXX
  ------------------>
  line 25 and 26 will be removed.
  """
    to_write_lines = []
    for i, line in enumerate(code):
        if line.startswith('parl.connect'):
            continue
        if i < end_of_file - 1:
            to_write_lines.append(line)
        else:
            break
    return to_write_lines


def load_remote_class(file_name, class_name, end_of_file):
  """
  load a class given is file_name and class_name.

  Args:
    file_name: specify the file to load the class
    class_name: specify the class to be loaded
    end_of_file: line ID to indicate the last line that defines the class.

  Return:
    cls: the class to load
  """
    with open(file_name) as t_file:
        code = t_file.readlines()
    code = simplify_code(code)
    tmp_file_name = 'xparl_' + file_name
    with open(tmp_file_name, 'w') as t_file:
        for line in code:
            t_file.write(line)
    mod = __import__(tmp_file_name)
    cls = getattr(mod, class_name)._original
    return cls