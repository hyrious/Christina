import os
from subprocess import Popen, PIPE, STARTUPINFO, STARTF_USESHOWWINDOW

from sublime import *
from sublime_plugin import *
from sublime_lib import *
from .diff_match_patch import *

def is_available(view):
    file_name = view.file_name()
    if not file_name: return False
    _, extname = os.path.splitext(file_name)
    return extname in ['.c', '.cpp']

def sel(view):
    ret = []
    for region in view.sel():
        if not region.empty():
            ret.append(region)
    if not ret:
        ret.append(Region(0, view.size()))
    return ret

def make_format_command(view):
    command = ['clang-format']
    for region in sel(view):
        offset = min(region.a, region.b)
        length = abs(region.b - region.a)
        command.extend(['-offset', str(offset),
                        '-length', str(length)])
    command.extend(['-assume-filename', view.file_name() or '(none)'])
    return command

def get_encoding(view):
    subl_enc = view.encoding()
    if subl_enc == 'Undefined':
        subl_enc = 'UTF-8'
    return encodings.from_sublime(subl_enc)

def subproc(command, stdin=None):
    startupinfo = None
    if os.name == 'nt':
        startupinfo = STARTUPINFO()
        startupinfo.dwFlags = STARTF_USESHOWWINDOW
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)
    return proc.communicate(stdin)

def make_patch(view, edit, stdin, output):
    dmp = diff_match_patch()
    patch = dmp.patch_make(stdin, output)
    for obj in patch:
        point = obj.start1
        for i, text in obj.diffs:
            if i == 0:
                point += len(text)
            elif i == 1:
                view.insert(edit, point, text)
                point += len(text)
            elif i == -1:
                view.erase(edit, Region(point, point + len(text)))

class ClangFormatCommand(TextCommand):
    def is_enabled(self):
        return is_available(self.view)

    def run(self, edit):
        view = self.view
        command = make_format_command(view)
        encoding = get_encoding(view)
        stdin = view.substr(Region(0, view.size()))
        output, error = subproc(command, stdin.encode(encoding))
        if error: return print(error)
        output = output.decode(encoding)
        make_patch(view, edit, stdin, output)
