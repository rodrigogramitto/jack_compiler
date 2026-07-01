# Generates VM Code
from pathlib import Path

class VMWriter:
  def __init__(self, file_path):
    file = Path(file_path)
    self.out_file = file.with_suffix('.vm').resolve()
    open(self.out_file, "w").close()

  def print_command(self, command):
    with open(self.out_file, "a") as f:
      f.write(command)
      f.write('\n')

  def write_push(self, segment, index):
    cmd = f"push {segment} {index}"
    self.print_command(cmd)

  def write_pop(self, segment, index):
    cmd = f"pop {segment} {index}"
    self.print_command(cmd)

  def write_arithmetic(self, command):
    cmd = f"{command}"
    self.print_command(cmd)

  def write_label(self, label):
    cmd = f"label {label}"
    self.print_command(cmd)

  def write_goto(self, label):
    cmd = f"goto {label}"
    self.print_command(cmd)

  def write_if(self, label):
    cmd = f"if-goto {label}"
    self.print_command(cmd)

  def write_call(self, name, nArgs):
    cmd = f"call {name} {nArgs}"
    self.print_command(cmd)

  def write_function(self, name, nVars):
    cmd = f"function {name} {nVars}"
    self.print_command(cmd)

  def write_return(self):
    cmd = f"return"
    self.print_command(cmd)