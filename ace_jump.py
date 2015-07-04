import sublime, sublime_plugin
import re, itertools

LABELS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

last_index = 0
hints = []
search_regex = r''

next_search = False

def get_active_views(window):
    """Returns all currently visible views"""

    views = []
    for group in range(window.num_groups()):
        views.append(window.active_view_in_group(group))
    return views

def set_views_syntax(views, syntax):
    """Sets the syntax highlighting for all given views"""

    for i in range(len(views)):
        views[i].set_syntax_file(syntax[i])

def get_views_syntax(views):
    """Returns a list with syntax for each from the given views"""

    syntax = []
    for view in views:
        syntax.append(view.settings().get('syntax'))
    return syntax

class AceJumpCommand(sublime_plugin.WindowCommand):
    """Base command class for AceJump plugin"""

    def run(self):
        self.char = ""
        self.target = ""
        self.views = []
        self.changed_views = []
        self.breakpoints = []

        self.all_views = get_active_views(self.window)
        self.syntax = get_views_syntax(self.all_views)

        self.show_prompt(self.prompt(), self.init_value())

    def show_prompt(self, title, value):
        """Shows a prompt with the given title and value in the window"""
        self.window.show_input_panel(
            title, value,
            self.next_batch, self.on_input, self.submit
        )

    def next_batch(self, command):
        """Displays the next batch of labels after pressing return"""

        self.remove_labels()
        self.show_prompt(self.prompt(), self.char)

    def on_input(self, command):
        """Fires the necessary actions for the current input"""

        if len(command) == 1:
            self.char = command
            self.add_labels(self.regex().format(re.escape(self.char)))
            return

        if len(command) == 2:
            self.target = command[1]

        self.window.run_command("hide_panel", {"cancel": True})

    def submit(self):
        """Handles the behavior after closing the prompt"""

        global next_search
        next_search = False

        self.remove_labels()
        set_views_syntax(self.all_views, self.syntax)
        self.jump(LABELS.find(self.target))

    def add_labels(self, regex):
        """Adds labels to characters matching the regex"""

        global last_index, hints

        self.breakpoints = []

        last_index = 0
        hints = []

        self.views = self.all_views[:] if len(self.views) == 0 else self.views
        self.changed_views = []

        for view in self.views[:]:
            view.run_command("add_ace_jump_labels", {"regex": regex})
            self.breakpoints.append(last_index)
            self.changed_views.append(view)

            if next_search:
                break

            self.views.remove(view)

        set_views_syntax(self.all_views, list(itertools.repeat(
            "Packages/AceJump/AceJump.tmLanguage",
            len(self.all_views)
        )))

    def remove_labels(self):
        """Removes all previously added labels"""

        last_breakpoint = 0
        for breakpoint in self.breakpoints:
            if breakpoint != last_breakpoint:
                view = self.changed_views[self.view_for_index(breakpoint - 1)]
                view.run_command("remove_ace_jump_labels")
                last_breakpoint = breakpoint

    def jump(self, index):
        """Performs the jump action"""

        if self.target == "" or index < 0 or index >= last_index:
            return

        region = hints[index].begin()
        view = self.changed_views[self.view_for_index(index)]

        self.window.focus_view(view)
        view.run_command("perform_ace_jump", {"target": region})

    def view_for_index(self, index):
        """Returns a view index for the given label index"""
        for breakpoint in self.breakpoints:
            if index < breakpoint:
                return self.breakpoints.index(breakpoint)

class AceJumpWordCommand(AceJumpCommand):
    """Specialized command for word-mode"""

    def prompt(self):
        return "Head char"

    def init_value(self):
        return ""

    def regex(self):
        return r'\b{}'

class AceJumpCharCommand(AceJumpCommand):
    """Specialized command for char-mode"""

    def prompt(self):
        return "Char"

    def init_value(self):
        return ""

    def regex(self):
        return r'{}'

class AceJumpLineCommand(AceJumpCommand):
    """Specialized command for line-mode"""

    def prompt(self):
        return ""

    def init_value(self):
        return " "

    def regex(self):
        return r'(.*)[^\s](.*)\n'

class AddAceJumpLabelsCommand(sublime_plugin.TextCommand):
    """Command for adding labels to the views"""

    def run(self, edit, regex):
        global hints

        characters = self.find(regex)

        self.add_labels(edit, characters)
        self.view.add_regions("ace_jump_hints", characters, "invalid")

        hints = hints + characters

    def find(self, regex):
        """Returns a list with all occurences matching the regex"""

        global next_search, last_index

        chars = []

        visible_region = self.view.visible_region()
        next_search = next_search if next_search else visible_region.begin()
        last_search = visible_region.end()

        while (next_search < last_search and last_index < len(LABELS)):
            word = self.view.find(regex, next_search)

            if not word:
                break

            last_index += 1
            next_search = word.end()
            chars.append(sublime.Region(word.begin(), word.begin() + 1))

        if last_index < len(LABELS):
            next_search = False

        return chars

    def add_labels(self, edit, regions):
        """Replaces the given regions with labels"""

        for i in range(len(regions)):
            self.view.replace(
                edit, regions[i], LABELS[last_index + i - len(regions)]
            )

class RemoveAceJumpLabelsCommand(sublime_plugin.TextCommand):
    """Command for removing labels from the views"""

    def run(self, edit):
        self.view.erase_regions("ace_jump_hints")
        self.view.end_edit(edit)
        self.view.run_command("undo")

class PerformAceJumpCommand(sublime_plugin.TextCommand):
    """Command performing the jump"""
    def run(self, edit, target):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        self.view.show(target)
