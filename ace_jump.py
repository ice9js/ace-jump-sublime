import sublime, sublime_plugin

LABELS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

last_index = 0
hints = []
search_regex = r''

next_search = False

class AceJumpCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.char = ""
        self.target = ""
        self.views = []
        self.all_views = []
        self.changed_views = []
        self.breakpoints = []

        for group in range(self.window.num_groups()):
            self.all_views.append(self.window.active_view_in_group(group))

        self.window.show_input_panel(
            self.prompt(),
            self.init_value(),
            self.submit,
            self.parse,
            self.jump
        )

    def submit(self, command):
        self.jump()
        self.window.show_input_panel(
            self.prompt(),
            self.char,
            self.submit,
            self.parse,
            self.jump
        )

    def parse(self, command):
        global search_regex

        search_regex = self.label_regex()

        if len(command) == 1:
            self.char = command
            self.search_views()
            return

        if len(command) == 2:
            self.target = command[1]

        self.window.run_command("hide_panel", {"cancel": True})

    def search_views(self):
        global last_index, hints

        self.breakpoints = []

        last_index = 0
        hints = []

        self.views = self.all_views[:] if len(self.views) == 0 else self.views
        self.changed_views = []

        for view in self.views[:]:
            view.run_command("add_ace_jump_labels", {"char": self.char})
            self.breakpoints.append(last_index)
            self.changed_views.append(view)

            if next_search:
                break

            self.views.remove(view)

    def jump(self):
        global next_search

        last_breakpoint = 0

        for breakpoint in self.breakpoints:
            if breakpoint != last_breakpoint:
                view = self.changed_views[self.view_for_index(breakpoint - 1)]
                view.run_command("remove_ace_jump_labels")
                last_breakpoint = breakpoint

        target_index = LABELS.find(self.target)

        if self.target == "" or target_index < 0:
            return

        target_region = hints[target_index].begin()
        target_view = self.changed_views[self.view_for_index(target_index)]

        self.window.focus_view(target_view)
        target_view.run_command("perform_ace_jump", {"target": target_region})

        next_search = False

    def view_for_index(self, index):
        for breakpoint in self.breakpoints:
            if index < breakpoint:
                return self.breakpoints.index(breakpoint)

class AceJumpWordCommand(AceJumpCommand):
    def prompt(self):
        return "Head char"

    def init_value(self):
        return ""

    def label_regex(self):
        return r'\b{}'

class AceJumpCharCommand(AceJumpCommand):
    def prompt(self):
        return "Char"

    def init_value(self):
        return ""

    def label_regex(self):
        return r'{}'

class AceJumpLineCommand(AceJumpCommand):
    def prompt(self):
        return ""

    def init_value(self):
        return " "

    def label_regex(self):
        return r'(.*)[^\s](.*)\n'

class AddAceJumpLabelsCommand(sublime_plugin.TextCommand):
    def run(self, edit, char):
        global next_search, last_index

        visible_region = self.view.visible_region()
        next_search = next_search if next_search else visible_region.begin()
        last_search = visible_region.end()

        while (next_search < last_search and last_index < len(LABELS)):
            word = self.view.find(search_regex.format(char), next_search)

            if not word:
                break

            label = LABELS[last_index]
            last_index += 1

            hint = sublime.Region(word.begin(), word.begin() + 1)
            hints.append(hint)

            self.view.replace(edit, hint, label)

            next_search = word.end()

        if last_index < len(LABELS):
            next_search = False

        self.view.add_regions("ace_jump_hints", hints, "invalid")

class RemoveAceJumpLabelsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase_regions("ace_jump_hints")
        self.view.end_edit(edit)
        self.view.run_command("undo")

class PerformAceJumpCommand(sublime_plugin.TextCommand):
    def run(self, edit, target):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(target))
        self.view.show(target)
