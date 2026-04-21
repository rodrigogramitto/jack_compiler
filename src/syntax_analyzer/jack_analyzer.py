from pathlib import Path
from src.syntax_analyzer.jack_tokenizer.tokenizer import JackTokenizer
from src.syntax_analyzer.compilation_engine.compiler import CompilationEngine

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
    with open(output_file, "w") as out_file:
      tokenizer = JackTokenizer(file)
      compilation_engine = CompilationEngine(tokenizer, out_file)
      compilation_engine.compile_class()

  def compile_dir(self, directory):
    # needs to make an output dir too
    for file_path in directory.iterdir():
      self.compile_file(file_path)