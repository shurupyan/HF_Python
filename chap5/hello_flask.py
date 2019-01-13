from flask import Flask, render_template, request
from vsearch import search4letters
from datetime import datetime
from flask import escape
from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': 'localhost',
            'user': 'vsearch',
            'password': 'vsearchpasswd',
            'database': 'vsearchlogDB',}


@app.route('/search4', methods=['POST', 'GET'])
def do_search() -> 'html':
    phrase=request.form['phrase']
    letters=request.form['letters']
    result = str(search4letters(phrase, letters))
    log_request(request, result)
    return render_template('results.html',
                           the_title='Here are your results:',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_result=result,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log() -> 'str':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select ts, phrase, letters, ip, browser_string, results from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Date', 'Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')    
    return render_template('viewlog.html',
                           the_title = 'View log',
                           the_row_titles = titles,
                           the_data = contents,)
    

def log_request(req: 'flask_request', res: str) ->None:

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

    
if __name__ == '__main__':
    app.run(debug=True)
