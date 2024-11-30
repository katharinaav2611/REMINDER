from akses_database import database_function as df 
from flask import Flask, request, redirect, url_for, render_template
import requests 
app = Flask(__name__)

data_user = []

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

@app.route('/', methods = ['POST', 'GET'])
def index():
    global data_user
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cek_username = df.check_data(username)
        if cek_username:
            data_user = df.get_user(username)
            if data_user[2] == password:
                return redirect(url_for('homepage'))
            else:
                # password salah 
                return render_template('index.html')
        else:
            # No username 
            return render_template('index.html') 

    return render_template('index.html')

@app.route('/SignUp', methods = ['POST', 'GET'])
def SignUp():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        check_username = df.check_data(username)
        
        if check_username == 0:    
            df.insert_user(username, password)
            return redirect(url_for('index'))
        else:
            return render_template('SignUp.html',message = "Username Telah digunakan, coba lagi")
    return render_template('SignUp.html')


@app.route('/homepage', methods = ['POST', 'GET'])
def homepage():
    global data_user
    names = df.get_user_name_all()
    
    if request.method == 'POST':
        if 'add_event' in request.form:
            event_date = request.form.get('addevent_date')
            event_title = request.form.get('addevent_title')
            event_content = request.form.get('addevent_content')
            
            df.insert_event(data_user[1],event_date,event_title,event_content)
            
        if 'add_user' in request.form:
            event_name = request.form.get('adduser_name')
            event_date = request.form.get('adduser_date')
            event_title = request.form.get('adduser_title')
            event_content = request.form.get('adduser_content')
            
            if event_name in names:
                df.insert_event(event_name,event_date,event_title,event_content)
            
        if 'delete_event' in request.form:
            event_date = request.form.get('showevent_date')
            event_title = request.form.get('showevent_title')
            event_content = request.form.get('showevent_content')
            
            df.delete_event(data_user[1],event_date,event_title,event_content)
    
    df.update_event()
    events = df.get_events(data_user[1])
    
    return render_template('homepage.html', events = events, username = data_user[1])

if __name__ == "__main__":
    app.run(port=5000,debug=True)