from flask import *
from app import app

@app.route('/')
@app.route('/index.html')
def main():
  return render_template('index.html')