from flask import Flask, render_template, request, redirect, url_for, g, flash, session, escape
from forms import NewGameForm
import minesweeper as ms
import os

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
app.secret_key = os.urandom(24)

# attempting session game board
session['game_board'] = None
session['game_on'] = False


@app.route('/')
def start_page():
    flash(u"Start A New Game?")
    return redirect('/new_game')


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    form = NewGameForm()
    if form.validate_on_submit():
        rows = form.rows.data
        columns = form.columns.data
        mines = form.mines.data
        if mines < rows * columns:
            session['game_board'] = ms.create_game_board(rows, columns, mines=mines)
            session['game_on'] = True
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
    if not session['game_on']:
        redirect(url_for('new_game'))
    return render_template("board.html", game_board=session['game_board'])

@app.route('/select_space/<int:row>/<int:col>')
def select_space(row, col):
    session['game_board']
    session['game_on']

    if session['game_on']:
        if 0 <= row <= len(session['game_board']) and 0 <= col <= len(session['game_board'][0]):
            # Valid entry
            game_on, game_board = ms.update_board(session['game_board'], row, col)
        # Win state
        if ms.check_victory(session['game_board']):
            flash(u"You Win! Play Again?")
        # Continue state
        elif session['game_on']:
            return redirect(url_for('render_board'))
        # Lose state
        else:
            flash(u"You Lose! Play Again?")
    # Return to the new game page on win or lose
    session.pop('game_board', 'game_on', None)
    return redirect(url_for('new_game'))



if __name__ == '__main__':
    app.run()
