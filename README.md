# Griddlers
Python scripts to generate a nonogram/griddler puzzle from a supplied png image.

## Background
Griddlers a.k.a. nonograms are a fun visual puzzle in which you reconstruct a small image. I discovered them on [Griddlers.net](https://www.griddlers.net/home) and after a few slow attempts at creating my own puzzles by hand, I decided it'd be fun to try to automate the process. The result is this collection of Python functions.

## Dependencies
Intended to run with Python 3
Uses numpy for array manipulation
Uses matplotlib for image reading

A pre-bundled package like [Anaconda](https://www.anaconda.com/) is an easy way to get both of these dependencies if you don't want to manually install them.

## How to use
Run the script from the command line as follows (navigate to the directory containing Nonogram.py and SvgFuncs.py):

  ``py Nonogram.py <input-image-path> <background-colour> <output-svg-path> [-s]``
  
Example:

  ``py Nonogram.py Smile.png #ffffff SmileGriddler.svg -s``

The background colour should be a hex rgb triple of the format #rrggbb. The optional -s flag is used to generate a solution image (already solved) instead of a puzzle image.

The included Windows command script demonstrates using the Nonogram.py script on the included Smile.png.
