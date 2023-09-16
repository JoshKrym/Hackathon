from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

directory = Path(__file__).parent

app=Flask(__name__)

@app.route('/')
def main():
    return render_template('/main.html')

if __name__ == '__main__':
    print("Hello World")

    app.run(debug=True)
