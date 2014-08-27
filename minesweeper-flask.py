from flask import Flask, render_template, request, redirect, url_for, g, flash
from forms import NewGameForm, GameOverForm
import minesweeper as ms

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

# global game board -- one player only
global game_board
game_board = None
global game_on
game_on = False


@app.route('/')
def start_page():
    # return "Hello World!"
    return redirect('/new_game')


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    form = NewGameForm()
    if form.validate_on_submit():
        rows = form.rows.data
        columns = form.columns.data
        mines = form.mines.data
        if mines < rows * columns:
            global game_board
            game_board = ms.create_game_board(rows, columns, mines=mines)
            global game_on
            game_on = True
            return redirect(url_for('render_board'))
        else:
            flash(u"You can't have more mines than spaces!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))

    return render_template('new_game.html', form=form)


@app.route('/board')
def render_board():
    if not game_on:
        redirect(url_for('new_game'))
    return render_template("board.html", game_board=game_board)

@app.route('/select_space/<int:row>/<int:col>')
def select_space(row, col):
    global game_board
    global game_on

    if game_on:
        if 0 <= row <= len(game_board) and 0 <= col <= len(game_board[0]):
            #Valid entry
            game_on, game_board = ms.update_board(game_board, row, col)
        if ms.check_victory(game_board):
            # add in a similar flashed message for if you win
            pass
        elif game_on:
            return redirect(url_for('render_board'))
        else:
            # remove this pass and replace it with something that will use the flashed messages system
            pass
    return redirect(url_for('new_game'))



if __name__ == '__main__':
    app.run()
