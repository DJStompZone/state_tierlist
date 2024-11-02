from flask import Flask, render_template

from util import STATE_HTML

app = Flask(__name__)

@app.route('/')
def state_tierlist():
    state_map = render_template('state_map.html', show_states=STATE_HTML)
    return render_template('index.html', state_map=state_map)

if __name__ == '__main__':
    app.run(debug=True)