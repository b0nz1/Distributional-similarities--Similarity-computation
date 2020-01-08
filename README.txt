1.to run similarities execute:
main.py coocurence_type file_name 

coocurence_type = 1 -> sentence coocurence
coocurence_type = 2 -> window coocurence
coocurence_type = 3 -> dependency coocurence

example: main.py 1 wikipedia.sample.trees.lemmatized

2. to run with w2v files execute:
python w2v.py bow5.words bow5.contexts
python w2v.py deps.words deps.contexts
