from src.syntax_analyzer.jack_tokenizer.library.symbols import  SYMBOLS
from src.syntax_analyzer.jack_tokenizer.library.keywords import KEYWORDS
from src.syntax_analyzer.jack_tokenizer.library.token_types import TokenType

class JackTokenizer:
  def __init__(self, file):
    self.input_file = file
    self.cursor = 0
    self.content = self.prepare_content()
    self.cur_token = ''
    self.advance()
    print("Cur token: ", self.cur_token)

  def has_more_tokens(self):
    local_cursor = self.cursor
    while local_cursor < len(self.content):
      if not self.content[local_cursor].isspace():
        return True
      local_cursor += 1
    return False

  def advance(self):
    cur = self.content[self.cursor]
    token = ''
    while cur.isspace():
      self.cursor += 1
      cur = self.content[self.cursor]
    if cur in SYMBOLS:
      self.cur_token = cur
    else:
      while not cur.isspace() and cur not in SYMBOLS:
        token += cur
        self.cursor += 1
        cur = self.content[self.cursor]
      self.cur_token = token

  def token_type(self):
    if self.cur_token in SYMBOLS:
      return TokenType.SYMBOL
    elif self.cur_token in KEYWORDS:
      return TokenType.KEYWORD


  def keyword(self):
    return

  def symbol(self):
    return

  def identifier(self):
    return

  def intval(self):
    return

  def stringval(self):
    return

  def prepare_content(self):
    prepared_content = []
    with open(self.input_file) as f:
      content = f.read()
      state = 'normal' # 'inline_comment', 'block_comment'
      i = 0
      while i < len(content):
        # normal state
        if state == 'normal':
          if content[i] == '/' and content[i + 1] == '/':
            state = 'inline_comment'
            i += 2
            continue
          elif content[i] == '/' and content[i + 1] == '*':
            state = 'block_comment'
            i += 2
            continue
          else:
            prepared_content.append(content[i])
            i += 1
        # Inline state
        elif state == 'inline_comment':
          if content[i] == '\n':
            state = 'normal'
          i += 1
        # Block State
        elif state == 'block_comment':
          if content[i] == '*' and content[i + 1] == '/':
            state = 'normal'
            i += 2
          else:
            i += 1

    return prepared_content


