

class JackAnalyzer:
  def __init__(self):
    return

  # Main module, for each file in the input it:
      # 1. creates a jackTokenizer from fileName.jack
      # 2. creates an output file named fileName.xml
      # 3. Creates a compilation engine, and calls the compileClass method
      #     (compileClass wil then do the rest of the parsing, recursively)
      # 4. Closes the output file.

      # # No api is given, implement own design.