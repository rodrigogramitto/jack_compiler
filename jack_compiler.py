import sys
import os

from src.syntax_analyzer.jack_analyzer import JackAnalyzer

def main():
  # Expect exactly one argument: the input path
  if len(sys.argv) != 2:
    print("Usage: python jack_compiler.py <input path>")
    sys.exit(1)

  input_path = sys.argv[1]
  JackAnalyzer(input_path)

if __name__ == "__main__":
  main()