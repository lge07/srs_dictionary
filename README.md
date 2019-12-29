# SRS Dictionary
*Notice: Currently Unfinished*

The included Python script, newdict.py, is meant to take information from https://github.com/open-dsl-dict/wiktionary-dict (specifically the Mandarin dictionary) and convert it to some usable Python data.

Data that I've generated is in the folder "div", for verification purposes. 

# Documentation
## Definition Class
The definition class is an attempt to hold all of the information I may need regarding how a term is defined. 

### Data
- `self.original` is a **string** that was fed to the class at creation.
- `self.english` is a **list** that contains the English word.
- `self.pos` is a **string** of the POS tag that was included. Not the type I'd like to use exactly, but good enough.
- `self.meta` is a **string** of the extra data regarding the scenario of the word.
- `self.chinese` is a **list** that contains the Chinese translations.
- `self.zh_extra` is a **list** that contains additional Chinese information given within parenthesis.
- `self.singleletter` is a **string** for verifying that the line isn't one of the single-letter pronounciations (see line 5 of en-cmn-enwiktionary.txt for an example).

### Parse Method
The parse method is fairly linear. Given the formatting of the definitions, it uses some regular expressions and simple character-in statements to look through what's going on. Expects a valid string.
- Splits into English/Chinese segments based on `::`
- Searches for Part-of-Speech (in `{}`), and more information (in `()`).
- Replaces POS and meta along with the spaces surrounding to get the actual English phrase.
- If `self.singleletter` is in the text, well, then search for and remove everything but the letter
- Otherwise, split by parenthesis, and look for what's simplified using the `hanzidentifier` library. Add to the list.

## Dictionary Class
The dictionary class is an attempt to contain and organise the definitions, and provide means of accessing a definition.

### Data
- `self.filename` is a **string** of the filename fed to the class at creation.
- `self.terms` is a **list** of ALL the terms. 

### d
d is meant to fill terms up with definitions. Expects a valid filename.
- Opens the file with UTF-8 encoding.
- Splits into lines
- Then goes through looking for the actual (non-commented) lines, which have `{` in them, and adding them to `self.terms`.

### div
div is meant to divide `self.terms` into files based on the first letter.
- Tries to create a new directory called `div` (whoops, I should remove my computer's file system from it :))
- Moves into that directory
- While the first letter is consistent, just add terms to a list of the same first letter.
- If not, well, time to clear the list, and dump.


