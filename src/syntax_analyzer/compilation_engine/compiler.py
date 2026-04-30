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
    self.statement_map = {
      # 'while': self.compile_while,
      # 'if': self.compile_if,
      # 'let': self.compile_let,
      # 'return': self.compile_return,
      'do': self.compile_do
    }
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
    self.indent_count -= 2
    self.write_tag(tag='classVarDec', closing=True, newline=True)



  def compile_subroutine(self):
    # Syntax rule:
    #   ('constructor' | 'function' | 'method')
    #   ('void' | type) subroutineName '('parameterList ')' subroutineBody

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

    self.write_tag(tag='subroutineDec', closing=True, newline=True)
    self.indent_count -= 2


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
    # Syntax Rule:
    # '{' varDec* statements '}'
    # 2. eat open brace
    # 3. invoke compile var dec
    # 4. invoke compile statements
    # 5. eat close brace
    # 6. write subroutine closing tag
    # 7. dedent
    self.write_tag(tag='subroutineBody', closing=False, newline=True)
    self.indent_count += 2
    self.eat( TokenType.SYMBOL, 'compile_subroutine_body', '{')

    while self.tokenizer.get_cur_token() == 'var':
      self.compile_var_dec()
    self.compile_statements()

    self.eat( TokenType.SYMBOL, 'compile_subroutine_body', '}')
    self.indent_count -= 2
    self.write_tag(tag='subroutineBody', closing=True, newline=True)


  def compile_var_dec(self):
    self.write_tag(tag='varDec', closing=False, newline=True)
    self.indent_count += 2

    self.eat( TokenType.KEYWORD, 'compile_var_dec', 'var' )
    if self.tokenizer.token_type() == TokenType.KEYWORD:
      self.eat( TokenType.KEYWORD, 'compile_var_dec', ['int', 'char', 'bool'] )
    else:
      self.eat( TokenType.IDENTIFIER, 'compile_var_dec')
    self.eat( TokenType.IDENTIFIER, 'compile_var_dec')

    while self.tokenizer.get_cur_token() == ',':
      self.eat( TokenType.SYMBOL, 'compile_var_dec', ',' )
      self.eat( TokenType.IDENTIFIER, 'compile_var_dec' )

    self.eat( TokenType.SYMBOL, 'compile_var_dec', ';')

    self.indent_count -= 2
    self.write_tag(tag='varDec', closing=True, newline=True)

  def compile_statements(self):
    while self.tokenizer.token_type() == TokenType.KEYWORD:
      if self.tokenizer.get_cur_token() not in self.statement_map:
        break
      else:
        self.statement_map[self.tokenizer.get_cur_token()]()

  def compile_let(self):
    return

  def compile_if(self):
    return

  def compile_while(self):
    return

  def compile_do(self):
    # Syntax rules
    # 'do' subroutineCall ';'

    self.write_tag(tag='doStatement', closing=False, newline=True)
    self.indent_count += 2

    self.eat( TokenType.KEYWORD, 'compile_do', 'do')

    self.eat( TokenType.IDENTIFIER, 'compile_do' )

    if self.tokenizer.get_cur_token() == '.' and self.tokenizer.token_type() == TokenType.SYMBOL:
        self.eat(TokenType.SYMBOL, 'compile_do', '.')
        self.eat(TokenType.IDENTIFIER, 'compile_do')

    self.eat(TokenType.SYMBOL, 'compile_do', '(')
    self.compile_expression_list()
    self.eat(TokenType.SYMBOL, 'compile_do', ')')
    self.eat(TokenType.SYMBOL, 'compile_do', ';')

    self.indent_count -= 2
    self.write_tag(tag='doStatement', closing=True, newline=True)

  def compile_return(self):
    return

  def compile_expression(self):
    return

  def compile_term(self):
    return

  def compile_expression_list(self):
    # Syntax Rule:
    #  (expression (',' expression)* )?

    self.write_tag(tag='compileExpression', closing=False, newline=True)
    self.indent_count += 2

    if self.tokenizer.get_cur_token() != ')':
      self.compile_term()
      while self.tokenizer.get_cur_token() == ',':
        self.eat(TokenType.SYMBOL, 'compile_expression_list', ',')
        self.compile_term()

    self.indent_count -= 2
    self.write_tag(tag='compileExpression', closing=True, newline=True)

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
    self.out_file.write( ' ' + token + ' ' )
    self.write_tag( TAGS[token_type], True )

    if self.tokenizer.has_more_tokens():
      self.tokenizer.advance()
      self.out_file.write('\n')

  # writes opening/closing non-terminal tags
  # todo: fix indentation crapout
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



