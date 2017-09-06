# AceJump

A plugin for Sublime Text 3 heavily inspired by AceJump for emacs.

AceJump allows you to move the cursor to any character to any place currently on screen.
To clarify, you can jump between characters in all visible portions of currently open documents in any panes.
Like it's emacs counterpart, AceJump for sublime features word (on the image below), character and line modes which make jumping even easier.

![AceJump](https://cloud.githubusercontent.com/assets/8056203/10858871/92069504-7f58-11e5-8593-e373121fd917.gif)

After selecting a mode, you type in a character (except in line mode, where you don't have to type in anything) and appropriate labels are displayed. Then all you need to do is press the key from the label and voila!

## Installation

### PackageControl

You can install AceJump from [PackageControl](http://wbond.net/sublime_packages/package_control) by following the steps below:

- Open up the command palette and select ```Package Control: Install Package```
- Wait for the packages index to load and select ```AceJump```

### Manual installation

You can install AceJump manually using git by running the following command within sublime packages directory (Preferences > Browse Packages):

```
$ git clone git@github.com:ice9js/ace-jump-sublime.git AceJump/
```

Or you can just copy the contents of this repository into ```Packages/AceJump```.

## Usage

### Word mode

Goes to a word starting with the given character. This mode works only with alphanumeric characters. If you're interested in jumping to a special character, use character mode instead.

- ```Ctrl/Super + Shift + ;```
- ```<head character>```
- ```<label>```

No need to press enter after selecting a label!

![Word mode](https://cloud.githubusercontent.com/assets/8056203/10858875/921aa814-7f58-11e5-99ec-9d17fc22f313.gif)

### Character mode

Goes to an occurence of the given character.

- ```Ctrl/Super + Shift + '```
- ```<character>```
- ```<label>```

![Character mode](https://cloud.githubusercontent.com/assets/8056203/10858870/92021b8c-7f58-11e5-916f-8ebc2d1d5eb4.gif)

### Line mode

Labels all non-empty lines and lets you jump to one of them.

- ```Ctrl/Super + Shift + .```
- ```<label>```

![Line mode](https://cloud.githubusercontent.com/assets/8056203/10858872/9207c596-7f58-11e5-9353-2d57783ca2cc.gif)

### Within Line mode

Labels all words within the line where current cursor locate and lets you jump to one of them.

- ```Ctrl/Super + Shift + ,```
- ```<label>```

### Select mode

After triggering select mode, the next jump will select everything inbetween the current cursor position and the selected label.
When select mode is triggered, the next jump is limited to the current file.

- ```Alt+;``` (```Ctrl+;``` for OS X)
- perform a jump using word, character or line mode

![Select mode](https://cloud.githubusercontent.com/assets/8056203/10858874/921207a4-7f58-11e5-936a-6e56ec80d486.gif)

***Note:*** To apply *Select mode* you must first start one of the *jump modes*.  
That is, first start, for example, a *Word mode* (by default *ctrl+shift+;*), **then** start the *Select mode* (default: *alt+;*), **only now** enter the *head character* and choose the corresponding label.

### Multiple cursors mode

After triggering multiple cursors mode, the next jump will add a new cursor to the view instead of moving the existing one.
Again, when this mode is triggered, only jumps in the same file are available.

- ```Alt+'``` (```Ctrl+'``` for OS X)

![Multiple cursors mode](https://cloud.githubusercontent.com/assets/8056203/10858873/9207ee86-7f58-11e5-9251-e74bd64dbfed.gif)

***Note:*** To apply *Multiple cursors mode* you must first start one of the *jump modes*.  
That is, first start, for example, a *Word mode* (by default *ctrl+shift+;*), **then** start the *Multiple cursors mode* (default: *alt+'*), **only now** enter the *head character* and choose the corresponding label.

### Jump-after mode

In this mode, the cursor will jump behind the targeted instance. Unfortunetely,
this mode cannot be paired with select or multiple cursors mode yet.

- ```Alt+.``` (```Ctrl+.``` for OS X)

![Jump-after mode](https://cloud.githubusercontent.com/assets/8056203/10858868/91fb4b22-7f58-11e5-8bdf-b489c6bb7ee2.gif)

***Note:*** To apply *Jump-after mode* you must first start one of the *jump modes*.  
That is, first start, for example, a *Word mode* (by default *ctrl+shift+;*), **then** start the *Jump-after mode* (default: *alt+.*), **only now** enter the *head character* and choose the corresponding label.

### Batching

In case there are more places to jump to than labels available, labels will be batched and you can cycle through them by simply pressing enter.

![Batching](https://cloud.githubusercontent.com/assets/8056203/10858869/92006792-7f58-11e5-9ece-6b94d1016147.gif)

## Customization

In order to access AceJump settings, go to ```Preferences > Package Settings > AceJump > Settings - User```.

### Key bindings

Go to ```Preferences > Package Settings > AceJump > Key Bindings - User```.
You can then override the bindings for any of the following commands:

- ```ace_jump_word```
- ```ace_jump_char```
- ```ace_jump_line```
- ```ace_jump_within_line```
- ```ace_jump_select```
- ```ace_jump_add_cursor```
- ```ace_jump_after```

The commands accept an optional Boolean `current_buffer_only` argument. When present and set to `true`, AceJump only performs on the currently edited buffer.

### Labels

You can override the ```labels``` setting to provide your own set of labels to be used by AceJump.

### Highlighting

You can also set the syntsx scope that's used for highlighting by overriding ```labels_scope```. The default scope is ```invalid```.

### Case sensitivity

Ace jump is case sensitive by default. Case sensitivity can be toggled on and off by altering the ```search_case_sensitivity``` setting.

### Jumping behind the last character in a line

By setting ```jump_behind_last_characters``` to ```true```, AceJump will jump behind a character if it's the last character on a line, without the need to trigger jump after mode. This only works in character mode and is switched off by default.
