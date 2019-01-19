from flask import Flask, render_template, request
from vsearch import search4letters

from flask import escape, session
from DBcm import UseDatabase, MyConnectionError, CredentialsError, SQlError
from checker import check_logged_in

app = Flask(__name__)
app.secret_key = 'YouWillNeverGuess'

app.config['dbconfig'] = {'host': 'localhost',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }


@app.route('/search4', methods=['POST', 'GET'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = str(search4letters(phrase, letters))

    try:
        log_request(request, result)
    except Exception as err:
        print('Error occured while writing to log! ', str(err))

    return render_template('results.html',
                           the_title='Here are your results:',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_result=result, )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'str':

    titles = ('Date', 'Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select ts, phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()

        return render_template('viewlog.html',
                               the_title='View log',
                               the_row_titles=titles,
                               the_data=contents, )
    except MyConnectionError as err:
        print('Database connection error!', str(err))
    except CredentialsError as err:
        print('Database username/password error!', str(err))
    except SQlError as err:
        print('Database SQL execution error!', str(err))
    except Exception as err:
        print('Error occured while reading the log! ', str(err))
    return 'Error'

def log_request(req: 'flask_request', res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
            (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout() -> str:
    if 'logged_in' in session:
        session.pop('logged_in')
    return 'You are now logged out'


if __name__ == '__main__':
    app.run(debug=True)
