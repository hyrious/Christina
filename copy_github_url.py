import sublime, sublime_plugin
import os


def copy_github_url(path, row) -> bool:
    base = ""
    remotes = dict()
    remote = "origin"
    for d in walk_up(path):
        base = d
        dot_git = os.path.join(d, ".git")
        if os.path.exists(dot_git):
            config = os.path.join(dot_git, "config")
            with open(config) as f:
                for line in f:
                    if line.startswith("[remote "):
                        remote = line[9:-3]
                    elif line.startswith("\turl = "):
                        url = line[7:-1]
                        remotes[remote] = url
            break
    if not remotes:
        return False

    if (remote := 'upstream') in remotes or (remote := 'origin') in remotes:
        url = remotes[remote]
    else:
        for name in remotes:
            url = remotes[name]
            break

    if url.endswith(".git"):
        url = url[0:-4]
    path = path[len(base):]
    url = url + "/blob/-" + path + "#L" + str(row + 1)
    sublime.set_clipboard(url)
    return True


def walk_up(path):
    curr = path
    while True:
        yield curr
        curr, tail = os.path.split(curr)
        if not tail:
            break


def lineno(view):
    selection = view.sel()
    if selection:
        i = selection[0].a
        row, col = view.rowcol(i)
        return row


class CopyGithubUrlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if len(self.view.file_name()) > 0:
            if (line := lineno(self.view)) is not None:
                if copy_github_url(self.view.file_name(), line):
                    sublime.status_message("Copied GitHub URL")

    def is_enabled(self):
        return self.view.file_name() is not None and len(self.view.file_name()) > 0
