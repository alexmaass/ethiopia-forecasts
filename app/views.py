from flask import *
from app import app

@app.route('/')
def main():
  return render_template('index.html')