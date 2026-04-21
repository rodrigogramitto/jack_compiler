from src.syntax_analyzer.jack_tokenizer.library.symbols import  SYMBOLS
from src.syntax_analyzer.jack_tokenizer.library.keywords import KEYWORDS
from src.syntax_analyzer.jack_tokenizer.library.token_types import TokenType
from decimal import Decimal
import re

class JackTokenizer:
  def __init__(self, file):
    self.input_file = file
    self.cursor = 0
    self.content = self.prepare_content()
    self.cur_token = ''

  def has_more_tokens(self):
    local_cursor = self.cursor
    while local_cursor < len(self.content):
      if not self.content[local_cursor].isspace():
        return True
      local_cursor += 1
    return False

  def advance(self):
    if self.cursor >= len(self.content):
      return

    cur = self.content[self.cursor]

    # Skip whitespace
    while self.cursor < len(self.content) and cur.isspace():
      self.cursor += 1
      if self.cursor >= len(self.content):
        return
      cur = self.content[self.cursor]

    # Symbol
    if cur in SYMBOLS:
      self.cur_token = cur
      self.cursor += 1
      return

    token = ''
    if cur == '"':
      token += cur
      self.cursor += 1
      while self.cursor < len(self.content):
        cur = self.content[self.cursor]
        if cur == '"':
          token += cur
          self.cursor += 1
          break
        token += cur
        self.cursor += 1
    else:
      while self.cursor < len(self.content):
        cur = self.content[self.cursor]
        if cur.isspace() or cur in SYMBOLS:
          break
        token += cur
        self.cursor += 1

    self.cur_token = token

  def token_type(self):
    if self.cur_token in SYMBOLS:
      return TokenType.SYMBOL
    elif self.cur_token in KEYWORDS:
      return TokenType.KEYWORD
    elif self.cur_token[0] == '"' and self.cur_token[-1] == '"':
      return TokenType.STRING_CONST
    elif self.is_int_constant():
      return TokenType.INT_CONST
    elif self.is_valid_identifier():
      return TokenType.IDENTIFIER
    else:
      return None

  def keyword(self):
    return self.cur_token

  def symbol(self):
    return self.cur_token

  def identifier(self):
    return self.cur_token

  def intval(self):
    return float(self.cur_token)

  def stringval(self):
    return self.cur_token

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

  def is_int_constant(self):
    try:
      float(self.cur_token)
      return True
    except ValueError:
      return False

  def is_valid_identifier(self):
    regex = r'^[A-Za-z_][A-Za-z0-9_]*$'
    return bool(re.match(regex, self.cur_token))

  def get_cur_token(self):
    return self.cur_token