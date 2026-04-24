from src.syntax_analyzer.jack_tokenizer.library.token_types import TokenType

TAGS = {
  TokenType.KEYWORD: 'keyword',
  TokenType.SYMBOL: 'symbol',
  TokenType.IDENTIFIER: 'identifier',
  TokenType.INT_CONST: 'integerConstant',
  TokenType.STRING_CONST: 'stringConstant'
}