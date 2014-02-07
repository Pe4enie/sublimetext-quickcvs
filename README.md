QuickCVS
=================

[Sublime Text 2](http://www.sublimetext.com/2) / [3](http://www.sublimetext.com/3) lightweight CVS plugin

---

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Development](#development-todo)


Installation
------------
Follow [this readme](https://github.com/ePages-rnd/sublimetext-plugins).


Features
--------

* Status
* Diff
* Update
* Get Clean Copy
* Commit
* Open folder in cervisia (Linux only)
* Visual diff (Unix only)
* Current status and branch displayed in the status bar

Usage
-------------
### Via Command Pallette
 * Bring up the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows).
 * Type `QuickCVS` to select `QuickCVS: status`, `QuickCVS: diff`,...

### Via Tools Menu
 * Tools **>** QuickCVS
 * Click `Status`, `Diff`,...

When using `Diff` you can jump through differences using `F4` / `Shift+F4` .

Development
-----------
* Implement `cvs annotate` to render output into file buffer.
* Open the current cartridge in a graphical CVS tool.
* Open folder in WinCVS resp. SmartCVS
