#!flask/bin/python
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/amaass'
db = SQLAlchemy(app)

@application.route('/')
@application.route('/index.html')
def main():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)