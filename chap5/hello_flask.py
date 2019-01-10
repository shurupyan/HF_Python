from flask import Flask, render_template, request
from vsearch import search4letters
from datetime import datetime
from flask import escape

app = Flask(__name__)


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
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Date', 'Form data', 'Remote_addr', 'User_agent', 'Results')    
    return render_template('viewlog.html',
                           the_title = 'View log',
                           the_row_titles = titles,
                           the_data = contents,)


def log_request(req: 'flask_request', res: str) ->None:
    with open('vsearch.log', 'a') as log:
        print(datetime.isoformat(datetime.today()), end='|', file=log)
        print(req.form, req.remote_addr, req.user_agent, res, sep='|', file=log)


if __name__ == '__main__':
    app.run(debug=True)
