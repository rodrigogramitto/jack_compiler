from pathlib import Path
from src.syntax_analyzer.jack_tokenizer.tokenizer import JackTokenizer
from src.syntax_analyzer.compilation_engine.compiler import CompilationEngine
from src.syntax_analyzer.compilation_engine.compiler_xml import XMLCompilationEngine


class JackAnalyzer:
  def __init__(self, input_path):
    path = Path(input_path)
    if path.is_file() and path.suffix == '.jack':
      self.compile_file(path)
    elif path.is_dir:
      self.compile_dir(path)

  def compile_file(self, file_path):
    file = file_path.resolve()
    filename = file_path.stem
    output_file = filename + '.xml'
    # TODO: remove xml and premature file creation
    with open(output_file, "w") as out_file:
      tokenizer = JackTokenizer(file)
      compilation_engine = CompilationEngine(tokenizer, out_file, file_path)
      xml_compilation_engine = XMLCompilationEngine(tokenizer, out_file, file_path)
      #compilation_engine.compile_class()
      xml_compilation_engine.compile_class()

  def compile_dir(self, directory):
    # needs to make an output dir too
    for file_path in directory.iterdir():
      if file_path.is_file() and file_path.suffix == '.jack':
        self.compile_file(file_path)