import os
import sys

from compilation_engine import CompilationEngine
from jack_tokenizer import JackTokenizer


class JackAnalyzer:
    def __init__(self, input_path, output_dir=None):
        self.input_path = input_path
        self.output_dir = output_dir

    def analyze(self):
        output_paths = []
        jack_files = self._find_jack_files()
        output_dir = self._get_output_dir()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for jack_file in jack_files:
            output_path = self._make_output_path(jack_file, output_dir)
            tokenizer = JackTokenizer(jack_file)
            compilation_engine = CompilationEngine(tokenizer, output_path)
            compilation_engine.compileClass()
            output_paths.append(output_path)

        return output_paths

    def _find_jack_files(self):
        if os.path.isfile(self.input_path):
            return [self.input_path]

        jack_files = []
        file_names = os.listdir(self.input_path)

        for file_name in file_names:
            if file_name.endswith(".jack"):
                jack_files.append(os.path.join(self.input_path, file_name))

        return jack_files

    def _get_output_dir(self):
        if self.output_dir is not None:
            return self.output_dir

        if os.path.isfile(self.input_path):
            input_dir = os.path.dirname(self.input_path)
        else:
            input_dir = self.input_path

        return os.path.join(input_dir, "output")

    def _make_output_path(self, jack_file, output_dir):
        file_name = os.path.basename(jack_file)
        base_name = file_name[:-5]
        output_file_name = base_name + ".xml"
        return os.path.join(output_dir, output_file_name)


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python jack_analyzer.py FILE_OR_DIRECTORY [OUTPUT_DIRECTORY]")
        return

    output_dir = None
    if len(sys.argv) == 3:
        output_dir = sys.argv[2]

    analyzer = JackAnalyzer(sys.argv[1], output_dir)
    output_paths = analyzer.analyze()

    for output_path in output_paths:
        print(output_path)


if __name__ == "__main__":
    main()
