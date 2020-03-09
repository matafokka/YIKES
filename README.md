# YIKES
Yes, Intelligent Kicking Expert System

# What it does?
It solves problems written by you or anyone else.

YIKES will show you all installed problems, click "Start" on any of those to start a solving.

Program will ask you a few questions, you should answer to all of them.

At the end, program will show you your results.

# How it works?
This is a rule-based system where each result is associated with a set of tags. That makes a full rule.

1. When user answers question, they "chooses" tags.
1. After all questions has been answered, program goes through each results and checks if it contains all "chosen" tags.
1. If it does, than the result will be presented to the user.
1. If it doesn't, than the result is dismissed.

# How do I create my own problem?
Check problems/example/ directory.

There's ReadMe.txt explaining problem's structure, but anyways:
* questions.xml	-- XML file containing questions for the user.
* results.csv		-- CSV file containing answers.

These files provides full tutorial with examples and everything, so you could start creating in almost no time!
