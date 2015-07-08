# AceJump

A plugin for Sublime Text 3 heavily inspired by AceJump for emacs.

AceJump allows you to move the cursor to any character to any place currently on screen.
To clarify, you can jump between characters in all visible portions of currently open documents in any panes.
Like it's emacs counterpart, AceJump for sublime features word (on the image below), character and line modes which make jumping even easier.

![AceJump Word Mode Labels](http://crystalplanet-studio.com/img/acejump/acejump.jpg)

After selecting a mode, you type in a character (except in line mode, where you don't have to type in anything) and appropriate labels are displayed. Then all you need to do is press the key from the label and voila!

## Installation

You can install AceJump for sublime using git by running the following command within sublime packages directory (Preferences > Browse Packages):

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

### Character mode

Goes to an occurence of the given character.

- ```Ctrl/Super + Shift + '```
- ```<character>```
- ```<label>```

### Line mode

Labels all non-empty lines and lets you jump to one of them.

- ```Ctrl/Super + Shift + l```
- ```<label>```

### Select mode

After triggering select mode, the next jump will select everything inbetween the current cursor position and the selected label.
When select mode is triggered, the next jump is limited to the current file.

- ```Alt+;``` (```Ctrl+;``` for OS X)
- perform a jump using word, character or line mode

### Multiple cursor mode

After triggering multiple cursor mode, the next jump will add a new cursor to the view instead of moving the existing one.
Again, when this mode is triggered, only jumps in the same file are available.

- ```Alt+'``` (```Ctrl+'``` for OS X)

### Batching

In case there are more places to jump to than labels available, labels will be batched and you can cycle through them by simply pressing enter.

## Customization

### Custom key bindings

If you wish to create your own bindings, you should bind them to these commands:

- ace_jump_word
- ace_jump_char
- ace_jump_line
- ace_jump_select
- ace_jump_add_cursor
