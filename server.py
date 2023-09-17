from flask import Flask, render_template, request, redirect, url_for, session
from pathlib import Path
from flask_session import Session
import json
from os import mkdir, SEEK_END, SEEK_SET

directory = Path(__file__).parent

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def main():
    session['username'] = 'Josh'
    return render_template('/home.html')

@app.route('/post.html')
def post():
    return render_template('/post.html')

@app.route('/newPost', methods=['POST'])
def newPost():
    print(request.form)
    userPosts = {}
    PostsFile = None
    print(f'./UserPosts/{session["username"]}.json')
    try:
        PostsFile = open(f'./UserPosts/{session["username"]}.json', 'r+')
    except(FileNotFoundError):
        PostsFile = open(f'./UserPosts/{session["username"]}.json', 'w+')
        PostsFile.write("{\n}")
    postData = request.form.to_dict()
    #postDataString = f', "{postData.pop("title")}" : {json.dumps(postData)}\n'
    Posts = json.loads(PostsFile.read())
    Posts[postData.pop("title")] = postData
    #if title already exists, send error
    print(json.dumps(Posts))
    PostsFile.seek(0)
    PostsFile.write(json.dumps(Posts))
    print(session['username'])
    PostsFile.close()
    return redirect('/yourPage.html')

@app.route('/yourPage.html')
def yourPage():
    return render_template('/yourPage.html')

if __name__ == '__main__':
    print("Hello World")

    app.run(debug=True)
