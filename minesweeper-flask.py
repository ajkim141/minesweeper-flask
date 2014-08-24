from flask import Flask, render_template, request, redirect, url_for
from minesweeper import NewGameForm

app = Flask(__name__)
app.debug = True
app.config.from_object('config')


@app.route('/')
def start_page():
    #return "Hello World!"
    return redirect('/new_game')

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    form = NewGameForm()
    if form.validate_on_submit():
        rows = form.rows.data
        columns = form.columns.data
        mines = form.mines.data
        return redirect(url_for('render_board'))
    return render_template('new_game.html', form=form)


@app.route('/board')
def render_board():
    return None

# @app.route('/select_space') #/<row>/<col>')
# def render_board(row, col):
#     return render_template("board.html", row, col)

# @app.route('/board/<row>/<col>')
# def select_space(row, col):
#     # do something
#     return None


if __name__ == '__main__':
    app.run()
