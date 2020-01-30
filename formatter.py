import sublime
from .formatters.phpformatter import PhpFormatter

class Formatter:
    def __init__(self, view):
        self.view = view

    def availableFormatters(self):
        return {
            'php': PhpFormatter()
        }

    def supportsSyntax(self, syntax):
        return syntax in self.availableFormatters().keys()

    def formatter(self, syntax):
        return self.availableFormatters().get(syntax)

    def format(self, syntax):
        code = self.view.substr(sublime.Region(0, self.view.size()))

        return self.formatter(syntax).format(code)