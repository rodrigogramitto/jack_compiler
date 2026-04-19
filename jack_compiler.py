import sys
import os

from src.syntax_analyzer import jack_analyzer

def main():
  # Expect exactly one argument: the input path
  if len(sys.argv) != 2:
    print("Usage: python jack_compiler.py <input path>")
    sys.exit(1)

    input_path = sys.argv[1]
    jack_analyzer(input_path)


if __name__ == "__main__":
  main()