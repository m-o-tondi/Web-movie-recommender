To run system, in command line/terminal, navigate to directory containing files Rec2.py, json_io.py, and folders static, ml-latest-small, and templates and type 

	"python3 json_io.py"

you will see 

	 * Serving Flask app "json_io" (lazy loading)
	 * Environment: production
	   WARNING: This is a development server. Do not use it in a production deployment.
	   Use a production WSGI server instead.
	 * Debug mode: on
	 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	 * Restarting with stat
	 * Debugger is active!
	 * Debugger PIN: 206-410-689

copy the http address (in this case 'http://127.0.0.1:5000/') into the url bar on your browser to be directed towards the "login" page.

Type in a number 1-610, corresponding to a userID who has rated a movie, and you will be directed to the home, or reccomendations page. Use dropdown boxes on each item to select a rating for a new item.  

In the navbar there is also "Already Rated". click on this to be sent to see all the books this user has already rated, and be allowed to change the rating on them, using dropdown boxes on each item.

 ============================SYSTEM FEATURES============================

200 words starts now:

Rec2.py: 

-	recommend_books() returns titles based on previous ratings and similar ratings of other users.
-	rating() allows users to post a new rating, or update an old one, and allows users to delete a rating if 0 rating is passed.
-	already_rated() returns all the titles the user has already rated.

Json_io.py is the flask middleman of the system. It sets up the “website” and then processes the AJAX get and post requests. Returns ‘/login’ until userID has been given.

Once “logged in” we have
-	‘/home’, which uses recommend_books() to give recommendations. 
-	‘/rating’, a page where the user can see all their previous ratings (through already_rated from Rec2.py).

Both pages use app_route /receiver, which allows the user to process post requests to the Rec2.py function rating().

The html and css files are very simple but do the job effectively. There are pages home.html, rated.html, and login.html, all implementing layout.html. 

login.html has form for userID input. 

home.html and rating.html are almost identical, and aside from the sources they get data from (recommend_books and already_rated respectively), only differ where already_rated provides user with current rating of title. 

If user chooses ‘Rate…’ on dropdown, rating for that title is deleted.

