from src.syntax_analyzer.compilation_engine.library.tags import TAGS

class CompilationEngine:
  def __init__(self, tokenizer, out_file):
    self.tokenizer = tokenizer
    self.out_file = out_file
    self.tokenizer.advance()

  def compile_class(self):
    # compiles an entire class
    # follow the rule (maybe make a rules lib that imports the current rule ex class into the function to follow the function left to right)
    # if the current 'portion' of the rule specifies a non-terminal rule xxx, call compilexxx -> this continues recursively
    # terminal xxx are only varname, constant and op codes (specific subset of keiwords, +, -, =, >, <)

    # How to start?
      # 1. Record the fact that it's starting by printing  (eat) -> eat is the helper method that prints the current token with the right tag and advances the tokenizer the <class> tag xml on the output
      # 2. then inspect the current token, it should be 'class', if so we eat it.
      # 3. then we inspect the current token, it should be an identifier, if so we eat it.
      # 4. then we inspect the current token, it should be an open bracket '{', if so we eat it.
      # 6. loop while current token is keyword AND is in [constructor, method,function, field, static], if so, route through keyword -> compile method map
      # 7. then the next token has to be a closing bracket '}', if so we eat it
      # finally we return.
      # * if any of the steps are not the expected token we must raise an error. additionally the recursive compile methods we invoke will also raise errors if the statement they're compiling doesn't adhere to syntax rules
    self.write_tag('class')
    self.eat('class', 'compile_class')
    return

  def compile_class_var_dec(self):
    return

  def compile_subroutine(self):
    return

  def compile_parameter_list(self):
    return

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
  def eat(self, expect_token, caller):
    # 3. Output the token with the right XML markup
    # 4. Advance the tokenizer if there are more tokens
    if self.tokenizer.get_cur_token() != expect_token:
      raise ValueError("Expected token: ", expect_token, ' but received: ', self.tokenizer.get_cur_token(), ' while executing: ', caller)

    token = self.tokenizer.get_cur_token()
    return

  # writes opening/closing non-terminal tags
  def write_tag(self, tag):
    xml = '<' + tag + '>'
    self.out_file.write( xml )


