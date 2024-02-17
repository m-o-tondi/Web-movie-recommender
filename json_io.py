from flask import Flask, request, flash, render_template, url_for, redirect, Response
import random, json
from Rec2 import recommend_books as rb
from Rec2 import rating as rat
from Rec2 import rated_already as ra

app = Flask(__name__)

@app.route("/")
def output():
	#userid = request.get_json(force=True)
	return render_template('login.html')

@app.route("/home")
def home():
	user = request.args.get('userid')
	if user is None:
		return render_template('login.html')
	else:
		number = int(user)
		return render_template('home.html', posts=rb(number,10))
	
@app.route("/rated")
def rated():
	user = request.args.get('userid')
	if user is None:
		return render_template('login.html')
	else:
		number = int(user)
		return render_template('rated.html', posts=ra(number))

@app.route('/receiver', methods = ['POST'])
def worker():
	data = request.get_json(force=True)
	info = data[0]
	rat(int(info['UserID']),int(info['BookID']),int(info['Rating']))
	return "done!"

if __name__ == '__main__':
	app.run(debug=True)
