
class SymbolTable:
  def __init__(self):
    self.fieldcount    = 0
    self.staticcount   = 0
    self.argumentcount = 0
    self.localcount    = 0
    self.entries = {}
    return

  def reset(self):
    self.fieldcount    = 0
    self.staticcount   = 0
    self.argumentcount = 0
    self.localcount    = 0
    self.entries = {}

  def define(self, name, type, kind):
    self.entries[name] = {
      'name': name,
      'type': type,
      'kind': kind,
      'index': self.var_count(kind)
    }
    self.increase_count(kind)

  def var_count(self, kind):
    if kind == 'field':
      return self.fieldcount
    elif kind == 'static':
      return self.staticcount
    elif kind == 'argument':
      return self.argumentcount
    elif kind == 'var':
      return self.localcount

  def increase_count(self, kind):
    if kind == 'field':
      self.fieldcount += 1
    elif kind == 'static':
      self.staticcount += 1
    elif kind == 'argument':
      self.argumentcount += 1
    elif kind == 'var':
      self.localcount += 1

  def kind_of(self, name):
    if name in self.entries:
      return self.entries[name]['kind']
    return None

  def type_of(self, name):
    if name in self.entries:
      return self.entries[name]['type']
    return None

  def index_of(self, name):
    if name in self.entries:
      return self.entries[name]['index']
    return None

  def get(self, name):
    if name in self.entries:
      return self.entries[name]
    return None