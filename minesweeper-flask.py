from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def start_page():
    #return "Hello World!"
    return render_template("new_game.html")

@app.route('/new_game')
def new_game():
    return None

@app.route('/board')
def render_board():
    return None

@app.route('/select_space') #/<row>/<col>')
def render_board(row, col):
    return render_template("board.html", row, col)

# @app.route('/board/<row>/<col>')
# def select_space(row, col):
#     # do something
#     return None


if __name__ == '__main__':
    app.run()
