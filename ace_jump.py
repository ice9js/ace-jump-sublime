import sublime, sublime_plugin
import re, itertools

last_index = 0
hints = []
search_regex = r''

next_search = False

# MODES
# 0: default (jumps in front of the selection)
# 1: select
# 2: add-cursor
# 3: jump-after
mode = 0

ace_jump_active = False

def get_active_views(window, current_buffer_only):
    """Returns all currently visible views"""

    views = []
    if current_buffer_only:
        views.append(window.active_view())
    else:
        for group in range(window.num_groups()):
            views.append(window.active_view_in_group(group))
    return views

def set_views_setting(views, setting, values):
    """Sets the values for the setting in all given views"""

    for i in range(len(views)):
        views[i].settings().set(setting, values[i])

def set_views_settings(views, settings, values):
    """Sets the values for all settings in all given views"""

    for i in range(len(settings)):
        set_views_setting(views, settings[i], values[i])

def get_views_setting(views, setting):
    """Returns the setting value for all given views"""

    settings = []
    for view in views:
        settings.append(view.settings().get(setting))
    return settings

def get_views_settings(views, settings):
    """Gets the settings for every given view"""

    values = []
    for setting in settings:
        values.append(get_views_setting(views, setting))
    return values

def set_views_syntax(views, syntax):
    """Sets the syntax highlighting for all given views"""

    for i in range(len(views)):
        views[i].set_syntax_file(syntax[i])

def set_views_sel(views, selections):
    """Sets the selections for all given views"""

    for i in range(len(views)):
        for sel in selections[i]:
            views[i].sel().add(sel)

def get_views_sel(views):
    """Returns the current selection for each from the given views"""

    selections = []
    for view in views:
        selections.append(view.sel())
    return selections

class AceJumpCommand(sublime_plugin.WindowCommand):
    """Base command class for AceJump plugin"""

    def run(self, current_buffer_only = False):
        global ace_jump_active
        ace_jump_active = True

        self.char = ""
        self.target = ""
        self.views = []
        self.changed_views = []
        self.breakpoints = []

        self.all_views = get_active_views(self.window, current_buffer_only)
        self.syntax = get_views_setting(self.all_views, "syntax")
        self.sel = get_views_sel(self.all_views)

        settings = sublime.load_settings("AceJump.sublime-settings")
        self.highlight = settings.get("labels_scope", "invalid")
        self.labels = settings.get(
            "labels",
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.case_sensitivity = settings.get("search_case_sensitivity", True)
        self.jump_behind_last = settings.get("jump_behind_last_characters", False)

        self.view_settings = settings.get("view_settings", [])
        self.view_values = get_views_settings(
            self.all_views,
            self.view_settings
        )

        self.show_prompt(self.prompt(), self.init_value())

    def is_enabled(self):
        global ace_jump_active
        return not ace_jump_active

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
        global next_search, mode, ace_jump_active
        next_search = False

        self.remove_labels()
        set_views_sel(self.all_views, self.sel)
        set_views_syntax(self.all_views, self.syntax)

        if self.valid_target(self.target):
            self.jump(self.labels.find(self.target))

        mode = 0
        ace_jump_active = False

    def add_labels(self, regex):
        """Adds labels to characters matching the regex"""

        global last_index, hints

        last_index = 0
        hints = []

        self.views = self.views_to_label()
        self.region_type = self.get_region_type()
        self.changed_views = []
        self.breakpoints = []
        changed_files = []

        for view in self.views[:]:
            if view.file_name() in changed_files:
                break

            view.run_command("add_ace_jump_labels", {
                "regex": regex,
                "region_type": self.region_type,
                "labels": self.labels,
                "highlight": self.highlight,
                "case_sensitive": self.case_sensitivity
            })
            self.breakpoints.append(last_index)
            self.changed_views.append(view)
            changed_files.append(view.file_name())

            if next_search:
                break

            self.views.remove(view)

        set_views_syntax(self.all_views, list(itertools.repeat(
            "Packages/AceJump/AceJump.tmLanguage",
            len(self.all_views)
        )))

        set_views_settings(
            self.all_views,
            self.view_settings,
            self.view_values
        )

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

        region = hints[index].begin()
        view = self.changed_views[self.view_for_index(index)]

        self.window.focus_view(view)
        view.run_command("perform_ace_jump", {"target": region})
        self.after_jump(view)

    def views_to_label(self):
        """Returns the views that still have to be labeled"""

        if mode != 0:
            return [self.window.active_view()]

        return self.all_views[:] if len(self.views) == 0 else self.views

    def view_for_index(self, index):
        """Returns a view index for the given label index"""

        for breakpoint in self.breakpoints:
            if index < breakpoint:
                return self.breakpoints.index(breakpoint)

    def valid_target(self, target):
        """Check if jump target is valid"""

        index = self.labels.find(target)

        return target != "" and index >= 0 and index < last_index;

    def get_region_type(self):
        """Return region type for labeling"""

        return "visible_region"

class AceJumpWordCommand(AceJumpCommand):
    """Specialized command for word-mode"""

    def prompt(self):
        return "Head char"

    def init_value(self):
        return ""

    def regex(self):
        return r'\b{}'

    def after_jump(self, view):
        global mode

        if mode == 3:
            view.run_command("move", {"by": "word_ends", "forward": True})
            mode = 0

class AceJumpCharCommand(AceJumpCommand):
    """Specialized command for char-mode"""

    def prompt(self):
        return "Char"

    def init_value(self):
        return ""

    def regex(self):
        return r'{}'

    def after_jump(self, view):
        global mode

        if mode == 3:
            view.run_command("move", {"by": "characters", "forward": True})
            mode = 0

    def jump(self, index):
        global mode

        view = self.changed_views[self.view_for_index(index)]
        if self.jump_behind_last and "\n" in view.substr(hints[index].end()):
            mode = 3

        return AceJumpCommand.jump(self, index)

class AceJumpLineCommand(AceJumpCommand):
    """Specialized command for line-mode"""

    def prompt(self):
        return ""

    def init_value(self):
        return " "

    def regex(self):
        return r'(.*)[^\s](.*)\n'

    def after_jump(self, view):
        global mode

        if mode == 3:
            view.run_command("move", {"by": "lines", "forward": True})
            view.run_command("move", {"by": "characters", "forward": False})
            mode = 0

class AceJumpWithinLineCommand(AceJumpCommand):
    """Specialized command for within-line-mode"""

    def prompt(self):
        return ""

    def init_value(self):
        return " "

    def regex(self):
        return r'\b\w'

    def after_jump(self, view):
        global mode

        if mode == 3:
            view.run_command("move", {"by": "word_ends", "forward": True})
            mode = 0

    def get_region_type(self):

        return "current_line"

class AceJumpSelectCommand(sublime_plugin.WindowCommand):
    """Command for turning on select mode"""

    def run(self):
        global mode

        mode = 0 if mode == 1 else 1

class AceJumpAddCursorCommand(sublime_plugin.WindowCommand):
    """Command for turning on multiple cursor mode"""

    def run(self):
        global mode

        mode = 0 if mode == 2 else 2

class AceJumpAfterCommand(sublime_plugin.WindowCommand):
    """Modifier-command which lets you jump behind a character, word or line"""

    def run(self):
        global mode

        mode = 0 if mode == 3 else 3

class AddAceJumpLabelsCommand(sublime_plugin.TextCommand):
    """Command for adding labels to the views"""

    def run(self, edit, regex, region_type, labels, highlight, case_sensitive):
        global hints

        characters = self.find(regex, region_type, len(labels), case_sensitive)
        self.add_labels(edit, characters, labels)
        self.view.add_regions("ace_jump_hints", characters, highlight)

        hints = hints + characters

    def find(self, regex, region_type, max_labels, case_sensitive):
        """Returns a list with all occurences matching the regex"""

        global next_search, last_index

        chars = []

        region = self.get_target_region(region_type)
        next_search = next_search if next_search else region.begin()
        last_search = region.end()

        while (next_search < last_search and last_index < max_labels):
            word = self.view.find(regex, next_search, 0 if case_sensitive else sublime.IGNORECASE)

            if not word or word.end() >= last_search:
                break

            last_index += 1
            next_search = word.end()
            chars.append(sublime.Region(word.begin(), word.begin() + 1))

        if last_index < max_labels:
            next_search = False

        return chars

    def add_labels(self, edit, regions, labels):
        """Replaces the given regions with labels"""

        for i in range(len(regions)):
            self.view.replace(
                edit, regions[i], labels[last_index + i - len(regions)]
            )

    def get_target_region(self, region_type):

        return {
            'visible_region': lambda view : view.visible_region(),
            'current_line': lambda view : view.line(view.sel()[0]),
        }.get(region_type)(self.view)

class RemoveAceJumpLabelsCommand(sublime_plugin.TextCommand):
    """Command for removing labels from the views"""

    def run(self, edit):
        self.view.erase_regions("ace_jump_hints")
        self.view.end_edit(edit)
        self.view.run_command("undo")

class PerformAceJumpCommand(sublime_plugin.TextCommand):
    """Command performing the jump"""

    def run(self, edit, target):
        global mode
        if mode == 0 or mode == 3:
            self.view.sel().clear()

        self.view.sel().add(self.target_region(target))
        self.view.show(target)

    def target_region(self, target):
        if mode == 1:
            for cursor in self.view.sel():
                return sublime.Region(cursor.begin(), target)

        return sublime.Region(target)
