from enum import Enum, auto

class TokenType(Enum):
  KEYWORD = auto()
  SYMBOL = auto()
  IDENTIFIER = auto()
  INT_CONST = auto()
  STRING_CONST = auto()
