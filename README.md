# AceJump

A plugin for Sublime Text 3 heavily inspired by AceJump for emacs.

AceJump allows you to move the cursor to any character to any place currently on screen.
To clarify, you can jump between characters in all visible portions of currently open documents in any panes.
Like it's emacs counterpart, AceJump for sublime features word and character modes which can make this operation even easier. The line mode has been dropped because of the issue with limited labels number, described in known issues.

## Installation

At the moment only the only way to install the plugin is to do so manually.
To install AceJump, clone this repository into your Packages directory. (Preferences > Browse Packages)

## Usage

### Word mode

Goes to a word starting with the given character. This mode works only with alphanumeric characters. If you're interested in jumping to a special character, use character mode instead.

- ```Ctrl/Super + Shift + ;```
- ```<head character>```
- ```<label>```

No need to press enter after the second character!

### Character mode

Goes to an occurence of the given character.

- ```Ctrl/Super + Shift + '```
- ```<character>```
- ```<label>```

## Known issues

- As of right now, only one character labels are allowed. This means they run out after 62 occurences. Will be fixed in 1.0
