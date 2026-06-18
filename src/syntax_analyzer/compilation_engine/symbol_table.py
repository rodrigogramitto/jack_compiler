
class SymbolTable:
  def __init__(self):
    return

  def reset(self):
    # called when starting to compile subroutine declaration
    # Empties symbol table and sets four indices to 0
    return

  def define(self, name, type, kind):
    # Defines (adds to the table) a new variable of the given name, type and kind.
    # Assigns it to the index value of that kind, and adds 1 to the index
    return

  def var_count(self, kind):
    # returns the number of variables of the given kind already defined in the table.
    return

  def kind_of(self, name):
    # returns the kind of the named variable
    return

  def index_of(self, name):
    # returns the index of the named variable.