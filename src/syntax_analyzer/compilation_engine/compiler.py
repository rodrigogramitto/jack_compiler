from src.syntax_analyzer.compilation_engine.library.tags import TAGS
from src.syntax_analyzer.jack_tokenizer.library.token_types import TokenType
from src.syntax_analyzer.jack_tokenizer.library.keywords import KEYWORDS
from src.syntax_analyzer.jack_tokenizer.library.symbols import SYMBOLS
import textwrap

class CompilationEngine:
  def __init__(self, tokenizer, out_file):
    self.tokenizer = tokenizer
    self.out_file = out_file
    self.indent_count = 0
    self.tokenizer.advance()

  def compile_class(self):
    self.write_tag(tag='class', closing=False, newline=True)
    self.indent_count += 2

    # Eat class tokens
    self.eat(TokenType.KEYWORD ,'compile_class', ['class'])
    self.eat(TokenType.IDENTIFIER ,'compile_class')
    self.eat(TokenType.SYMBOL ,'compile_class', '{')

    # Recursively invoke class var declarations
    while self.tokenizer.token_type() == TokenType.KEYWORD and self.tokenizer.get_cur_token() in ['field', 'static']:
      self.compile_class_var_dec()

    # Recursively invoke subroutine declarations
    if self.tokenizer.token_type() == TokenType.KEYWORD and self.tokenizer.get_cur_token() in ['constructor', 'method', 'function']:
      self.compile_subroutine()

    # self.eat(TokenType.SYMBOL ,'compile_class', '}')
    # self.write_tag(tag='class', closing=True, newline=False)
    # self.indent_count -= 2


  def compile_class_var_dec(self):
    self.write_tag(tag='classVarDec', closing=False, newline=True)
    self.indent_count += 2
    self.eat(TokenType.KEYWORD, 'compile_class_var_dec', ['static', 'field'])
    self.eat(TokenType.KEYWORD, 'compile_class_var_dec', ['var', 'int', 'char', 'boolean'])
    self.eat(TokenType.IDENTIFIER, 'compile_class_var_dec')

    while self.tokenizer.get_cur_token() == ',':
      self.eat(TokenType.SYMBOL, 'compile_class_var_dec', [','] )
      self.eat(TokenType.IDENTIFIER, 'compile_class_var_dec')

    self.eat(TokenType.SYMBOL, 'compile_class_var_dec', [';'] )
    self.write_tag(tag='classVarDec', closing=True, newline=True)

    self.indent_count -= 2

  def compile_subroutine(self):
    # Syntax rule:
    #   ('constructor' | 'function' | 'method')
    #   ('void' | type) subroutineName '('parameterList ')' subroutineBody

    # 1. Write Tag with subroutineDec
    # 2. Eat the next token expecting it to be keyword constructor, method or function
    # 3. Eat the type expecting it to be 'void', 'int', 'char', 'boolean' or if it's an identifier then identifier
    # 4. Eat the subroutine Name (identifier)
    # 5. tag (
    # 6. invoke compile parameter list
    # 7. tag )
    # 8. invoke compile subroutine body
    # 9. write closing tag
    self.write_tag(tag='subroutineDec', closing=False, newline=True)
    self.indent_count += 2

    self.eat( TokenType.KEYWORD ,'compile_subroutine', ['constructor', 'method', 'function'] )

    if self.tokenizer.token_type() == TokenType.KEYWORD:
      self.eat( TokenType.KEYWORD ,'compile_subroutine', ['void', 'int', 'char', 'boolean'] )
    else:
      self.eat( TokenType.IDENTIFIER ,'compile_subroutine' )

    self.eat( TokenType.IDENTIFIER ,'compile_subroutine' )
    self.eat(TokenType.SYMBOL ,'compile_subroutine', '(')
    self.compile_parameter_list()
    self.eat(TokenType.SYMBOL ,'compile_subroutine', ')')
    self.compile_subroutine_body()

  def compile_parameter_list(self):
    # ( (type varName) (',' type varName)*)?

    self.write_tag(tag='parameterList', closing=False, newline=True)

    if self.tokenizer.get_cur_token() != ')':

        if self.tokenizer.token_type() == TokenType.KEYWORD:
          self.eat( TokenType.KEYWORD ,'compile_parameter_list', ['void', 'int', 'char', 'boolean'] )
        else:
          self.eat( TokenType.IDENTIFIER ,'compile_parameter_list' )

        self.eat( TokenType.IDENTIFIER ,'compile_parameter_list' )

        while self.tokenizer.get_cur_token() == ',':
          self.eat(TokenType.SYMBOL, 'compile_parameter_list', [','] )
          self.eat(TokenType.IDENTIFIER, 'compile_parameter_list')

    self.write_tag(tag='parameterList', closing=True, newline=True)

  def compile_subroutine_body(self):
    return

  def compile_var_dec(self):
    return

  def compile_statements(self):
    return

  def compile_let(self):
    return

  def compile_if(self):
    return

  def compile_while(self):
    return

  def compile_do(self):
    return

  def compile_return(self):
    return

  def compile_expression(self):
    return

  def compile_term(self):
    return

  def compile_expression_list(self):
    return

  # Validates, writes terminal tags and advances
  def eat(self, expect_token_type, caller, expect_token_value=[]):
    token, token_type = self.tokenizer.get_cur_token(), self.tokenizer.token_type()

    if expect_token_value and token not in expect_token_value:
      raise ValueError("Expected token: ", expect_token_value, ' but received: ', token, ' while executing: ', caller)
    elif token_type != expect_token_type:
      raise ValueError("Expected token type: ", expect_token_type, ' but received: ', token_type, ' while executing: ', caller)
    elif expect_token_type == TokenType.IDENTIFIER and not self.tokenizer.is_valid_identifier():
      raise ValueError("Invalid identifier token: ", token, ' while executing: ', caller)

    self.write_tag( TAGS[token_type] )
    self.out_file.write( ' ' + token )
    self.write_tag( TAGS[token_type], True )

    if self.tokenizer.has_more_tokens():
      self.tokenizer.advance()
      self.out_file.write('\n')

  # writes opening/closing non-terminal tags
  def write_tag(self, tag, closing=False, newline=False):
    xml = '<'
    if closing:
      xml += '/'
    xml += tag + '>'

    indent = ' ' * self.indent_count
    xml = textwrap.indent(xml, indent)
    self.out_file.write( xml )
    if newline:
      self.out_file.write( '\n' )



