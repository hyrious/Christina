from sublime import *
from sublime_plugin import *
from pathlib import Path
import subprocess

class OpenTerminalCommand(TextCommand):
    def is_visible(self):
        return self.view.file_name() is not None

    def run(self, edit):
        path = Path(self.view.file_name()).parent
        subprocess.Popen('cmd.exe', cwd=str(path))
