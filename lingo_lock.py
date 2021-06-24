import duolingo
from yaml import safe_load
from requests import get
import urwid
from random import randrange
from subprocess import run
import signal

# Load YAML values
with open("/home/christopolise/CS_456/playing_around/config.yaml") as f:
    config = safe_load(f)

URL = config["esp32"]["addr"]

passwd = ""
word = ""
check = ""
lingo = duolingo.Duolingo

palette = [
    ('owl_art', '', '', '', 'g27', '#bff199'),
    ('title_style', '', '', '', 'black,bold', '#bff199'),
    ('bg', '', '', '', '#fff', '#071108'),
]

owl = [
    " __________",
    " / ___  ___ \\",
    "/ / @ \/ @ \ \\",
    " \ \___/\___/ /\\",
    "  \____\/____/||",
    "  /     /\\\\\//",
    "  |     |\\\\\\\\\\\\",
    "   \      \\\\\\\\\\\\",
    "    \______/\\\\\\\\",
    "_||_||_",
    "-- --"
]

owl_txt = []
question_widgets = []

def exit_on_esc(key):
    """
    Catches the escape key and exits
    @param key - character caught
    """
    if key == 'esc':
        raise urwid.ExitMainLoop()

def getWord():
    global lingo, word

    word = ""

    while len(word) < 5:
        word = lingo.get_known_words('el')[randrange(len(lingo.get_known_words('el')))]

    question_widgets[len(question_widgets) - 3].original_widget.set_text(word)
    question_widgets[len(question_widgets) - 1].original_widget._original_widget.set_edit_text("")
    pad.original_widget._set_original_widget(urwid.Filler(quest_pile)) 
    loop.draw_screen()

def checkTranslation(user_input):
    global word, check
    check = lingo.get_translations([user_input], source='en', target='el')

    for item in check[user_input]:
        try:
            num = item.index('(')
        except ValueError:
            num = -1
        if num != -1:
            if word == item[0:(item.index('(') - 1)]:
                # r = get(url=URL + "/correct")
                return True
        else:
            if word == item:
                # r = get(url=URL + "/correct")
                return True
    
    # r = get(url=URL + "/incorrect")
    return False
    

def login_duolingo():
    global username, passwd, lingo
    try:
        owl_txt[len(owl_txt) - 1].set_text("Checking credentials ")
        loop.draw_screen()
        lingo = duolingo.Duolingo(owl_txt[len(owl_txt) - 5].original_widget._original_widget.get_edit_text(), passwd)
        # r = get(url=URL + "/login_success")
        getWord()
    except duolingo.DuolingoException:
        # r = get(url=URL + "/login_fail")
        owl_txt[len(owl_txt) - 1].set_text("Incorrect Credentials")
        owl_txt[len(owl_txt) - 3].original_widget._original_widget.set_edit_text("")
        passwd = ""
        owl_txt[len(owl_txt) - 5].original_widget._original_widget.set_edit_text("")
        username = ""
        loop.draw_screen()


class UserBox(urwid.LineBox):
    def keypress(self, size, key):
        global username
        """
        Takes the size and key and processes the key press
        """
        return super(UserBox, self).keypress(size, key)
        
class PasswdBox(urwid.LineBox):
    def keypress(self, size, key):
        global passwd
        """
        Takes the size and key and processes the key press
        """

        # If the message isn't submitted keep typing
        if key != "enter": 
            return super(PasswdBox, self).keypress(size, key)
        
        passwd = self.original_widget.get_edit_text()
        login_duolingo()

class AnswerBox(urwid.LineBox):
    def keypress(self, size, key):
        global word
        """
        Takes the size and key and processes the key press
        """

        # If the message isn't submitted keep typing
        if key != 'enter':
            return super(AnswerBox, self).keypress(size, key)

        if checkTranslation(self.original_widget.get_edit_text()):
            raise urwid.ExitMainLoop()
        else:
             getWord()

# Title and spacer

owl_txt.append(urwid.AttrWrap(urwid.Text(" Lingo Lock ", 'center'), 'title_style'))

for i in range(3):
    owl_txt.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))

for line in owl:
    owl_txt.append(urwid.AttrWrap(urwid.Text(line, 'center'), 'owl_art'))

for i in range(3):
    owl_txt.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))

owl_txt.append(urwid.AttrWrap(UserBox(urwid.Edit(), 'Duolingo Username '), 'bg'))
owl_txt.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))
owl_txt.append(urwid.AttrWrap(PasswdBox(urwid.Edit(mask="*"), 'Password ﳳ'), 'bg'))
owl_txt.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))
owl_txt.append(urwid.AttrWrap(urwid.Text("", 'center'), 'title_style'))

pile = urwid.Pile(owl_txt)

fill = urwid.AttrWrap(urwid.Filler(pile), 'owl_art')
pad = urwid.AttrWrap(urwid.Padding(fill, 'center', right=20, left=20), 'owl_art')

question_widgets.append(urwid.AttrWrap(urwid.Text(" Translate the following word to unlock your computer ", 'center'),'title_style'))
question_widgets.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))
question_widgets.append(urwid.AttrWrap(urwid.Text("____________________________________________________", 'center'),'title_style'))
question_widgets.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))
question_widgets.append(urwid.AttrWrap(urwid.Text("", 'center'),'owl_art'))
question_widgets.append(urwid.AttrWrap(urwid.Divider(), 'title_style'))
question_widgets.append(urwid.AttrWrap(AnswerBox(urwid.Edit(), 'Translation 韛'), 'bg'))

quest_pile = urwid.Pile(question_widgets)


loop = urwid.MainLoop(
    pad,
    palette,
)
loop.screen.set_terminal_properties(colors=256)

def main():
    
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    # if run(['ping', '-c', '1', URL[7:]], capture_output=False).returncode:
    #     exit(1)
    
    loop.run()

if __name__ == "__main__":
    main()
