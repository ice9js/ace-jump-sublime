# AceJump

A plugin for Sublime Text 3 heavily inspired by AceJump for emacs.

AceJump allows you to move the cursor to any character to any place currently on screen.
To clarify, you can jump between characters in all visible portions of currently open documents in any panes.
Like it's emacs counterpart, AceJump for sublime features word, character and line modes which make jumping even easier.

## Installation

At the moment only the only way to install the plugin is to do so manually.
To install AceJump, clone this repository into your Packages directory. (Preferences > Browse Packages)
Make sure the directory is named *AceJump* and not *ace-jump-sublime*!

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

### Batching

In case there are more places to jump to than labels available, labels will be batched and you can cycle through them by simply pressing enter.

## Customization

### Custom key bindings

If you wish to create your own bindings, you should bind them to these commands:

- ace_jump_word
- ace_jump_char
- ace_jump_line

## Contributing

Feel free to create an issue to report a bug or if you have a feature proposal and I'll see what I can do about it. You're also welcome to send in any pull requests.

## Notes
