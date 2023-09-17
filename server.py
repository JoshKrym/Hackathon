from flask import Flask, render_template, request, redirect, url_for, session
from pathlib import Path
from flask_session import Session
import json
from os import mkdir, SEEK_END, SEEK_SET, path, listdir
from random import shuffle

directory = Path(__file__).parent

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def login():
    print(session['username'])
    if(session['username'] and session['username'] != None):
        return redirect('home.html')
    #session['username'] = 'Josh'
    return render_template('/login.html')

@app.route('/login.html')
def alsoLogin():
    print('here')
    return login()

@app.route('/createAccount.html')
def createAccount():
    #session['username'] = 'Josh'
    return render_template('basis.html', page = '/createAccount.html')

@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    print(request.form)
    Messages = {}
    messageList = []
    messageList.append(request.form['message'])
    Messages[session['username']] = messageList

    try:
        MessagesFile = open(f'./messages/{request.form["user"]}.json', 'r+')
    except(FileNotFoundError):
        MessagesFile = open(f'./messages/{request.form["user"]}.json', 'w+')
        MessagesFile.write("{\n}")
        MessagesFile.seek(0)
    Messages = json.loads(MessagesFile.read())
    try:
        messageList = Messages[session['username']]
    except(KeyError):
        Messages[session['username']] = messageList
    messageList.append(request.form['message'])
    Messages[session['username']] = messageList

    print(json.dumps(Messages))
    MessagesFile.seek(0)
    MessagesFile.write(json.dumps(Messages))
    
    return "thanks"

@app.route('/requesterProfiles.html/<accountName>')
def requesterProfiles(accountName):
    if not verifyLogin(): return redirect('/')
    print(accountName)
    PostsFile = None
    Posts = []
    try:
        PostsFile = open(f'./UserPosts/{accountName}.json', 'r')
        Posts = json.loads(PostsFile.read())
    except(FileNotFoundError):
        print('here')
    print(Posts)
    #postDataString = f', "{postData.pop("title")}" : {json.dumps(postData)}\n'
    for i in Posts:
        print(f"{i}, {Posts[i]}")
    return render_template('basis.html', page = 'requesterProfiles.html', Posts = Posts, User = accountName)

@app.route('/myProfile')
def myProfile():
    return redirect(f'/requesterProfiles.html/{session["username"]}')

@app.route('/verifyUser', methods=['POST'])
def verifyUser():
    UsersFile = open('Users.json', 'r')
    Users = json.loads(UsersFile.read())
    print(request.form)
    print(Users[request.form['Username']])
    print(request.form['Password'])
    if(Users[request.form['Username']] == request.form['Password']):
        session['username'] = request.form['Username']
        return redirect('/home.html')
    return "incorrect password"

@app.route('/messages.html')
def messages():
    Messages = {}
    try:
        MessagesFile = open(f'./messages/{session["username"]}.json', 'r')
        Messages = json.loads(MessagesFile.read())
        MessagesFile.close()
    except(FileNotFoundError):
        print('here')
    return render_template('basis.html', page = 'messages.html', Messages = Messages)
    


@app.route('/home.html')
def home():
    if not verifyLogin(): return redirect('/')
    Users = listdir('./UserPosts')
    Posts = {}
    for i in Users:
        PostsFile = open(f'./UserPosts/{i}', 'r')
        Post = json.loads(PostsFile.read())
        for j in Post:
            print(Post[j])
            Post[j]["User"] = i[:-5]
            Posts[j] = Post[j]
    print(Posts)
    return render_template('basis.html', page = 'home.html', Posts = Posts)
    #return render_template('/basis.html', page = 'home.html')


@app.route('/createUser', methods=['POST'])
def createUser():
    print(request.form)
    UserPassDict = {request.form['Username']:request.form['Password']}
    UsersFile = open('Users.json', 'r+')
    Users = json.loads(UsersFile.read())
    Users[request.form['Username']] = request.form['Password']
    UsersFile.seek(0,0)
    UsersFile.write(json.dumps(Users))
    session['username'] = request.form['Username']
    return redirect('/home.html')

@app.route('/post.html')
def post():
    if not verifyLogin(): return redirect('/')
    return render_template('basis.html', page = '/post.html')

@app.route('/logout', methods=['POST'])
def logout():
    session['username'] = None
    return "You have been successfully logged out."

@app.route('/newPost', methods=['POST'])
def newPost():
    print(request.form)
    print(request.files)
    userPosts = {}
    PostsFile = None
    print(f'./UserPosts/{session["username"]}.json')
    try:
        PostsFile = open(f'./UserPosts/{session["username"]}.json', 'r+')
    except(FileNotFoundError):
        PostsFile = open(f'./UserPosts/{session["username"]}.json', 'w+')
        PostsFile.write("{\n}")
        PostsFile.seek(0)
    postData = request.form.to_dict()
    image = request.files['image']
    postData["image"] = image.filename
    #postDataString = f', "{postData.pop("title")}" : {json.dumps(postData)}\n'
    Posts = json.loads(PostsFile.read())
    Posts[postData.pop("title")] = postData
    print(postData)
    #if title already exists, send error
    print(json.dumps(Posts))
    PostsFile.seek(0)
    PostsFile.write(json.dumps(Posts))
    print(session['username'])
    PostsFile.close()

    print(postData)

    
    image.save(path.join('./static/images', image.filename))

    return myProfile()

@app.route('/yourPage.html')
def yourPage():
    if not verifyLogin(): return redirect('/')
    return render_template('basis.html', page = '/yourPage.html')

def verifyLogin():
    print('here')
    return (session['username'] and session['username'] != None)

if __name__ == '__main__':
    print("Hello World")

    app.run(debug=True)
