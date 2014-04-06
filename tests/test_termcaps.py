import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from termcaps import tcaps as Tcaps

tcaps = Tcaps(True)

def test_start():
    print(tcaps.start("red","yellow","reverse")+"oooo"+tcaps.default())

def test_end():
    print(tcaps.start("red","yellow",\
        "reverse")+"oo"+tcaps.end(attribute="reverse")+"oo"+tcaps.default())

def test_default():
    print(tcaps.start("red","yellow",\
        "reverse")+"oo"+tcaps.default()+"oo")

def test_clear():
    print(tcaps.clear())

def test_move():
    print(tcaps.move_cursor(50,50)+"oo")

def test_reset_screen():
    print(tcaps.reset_screen())

def test_reset_cursor():
    print(tcaps.reset_cursor())
