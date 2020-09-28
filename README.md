# YIKES
Yes, Intelligent Kicking Expert System

[Here's a little demo on YouTube](https://youtu.be/ap2XUUo9TNg)

# What it does?
It solves problems written by you or anyone else.

YIKES will show you all installed problems. Click "Start" on any of those to solve it.

Program will ask you a few questions, you should answer all of them.

At the end, program will show you the results.

# How it works?
1. This is a rule-based system where each result is associated with a set of tags. That makes a full rule.
1. When user answer a question, they "choose" associated tags.
1. After all questions has been answered, program goes through each result and checks if it contains all "chosen" tags.
1. If it does, a result will be presented to the user.
1. If it doesn't, a result is dismissed.

# How do I install it?
In order to run this program, you'll need to install following stuff:
1. [Python 3 interpreter](https://www.python.org/)
1. PyQt5. You can download it from repos of your distro or run: `pip install PyQt5`. The last way is preferred for Windows.

Then:
1. Download and extract the source code.
1. `cd` to the extracted files.
1. Run `python yikes.py` or, if it doesn't work, `python3 yikes.py`.

# How do I create my own problems?
Check problems/example/ directory.

There's ReadMe.txt explaining problem's structure, but anyways:
* `questions.xml` - XML file containing questions for the user.
* `results.csv` - CSV file containing answers.

These files provides a full tutorial with examples and everything, so you could start creating in almost no time!
