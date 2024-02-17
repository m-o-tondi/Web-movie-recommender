#=======================================================================
#Implementation and adaptation of Matrix Factorisation 
#demonstrated by Nick Becker (RAPIDS Team at NVIDIA) at
#https://beckernick.github.io/matrix-factorization-recommender/
#=======================================================================

import pandas as pd
import numpy as np
import os

def rated_already(userID):
	ratings_list = [i.strip().split(",") for i in open('ml-latest-small/ratings.csv', 'r').readlines()]
	books_list = [i.strip().split(",") for i in open('ml-latest-small/books.csv', 'r').readlines()]

	ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'BookID', 'Rating'], dtype = int)
	books_df = pd.DataFrame(books_list, columns = ['BookID', 'Title', 'Genres'])

	books_df['BookID'] = books_df['BookID'].astype(int)
	ratings_df['BookID'] = ratings_df['BookID'].astype(int)
	ratings_df['UserID'] = ratings_df['UserID'].astype(int)
	ratings_df['Rating'] = ratings_df['Rating'].astype(float)

	user_data = ratings_df[ratings_df.UserID == (userID)]
	user_full = (user_data.merge(books_df, how = 'left', left_on = 'BookID', right_on = 'BookID').sort_values(['Rating'], ascending=False))
	user_full = user_full.drop(columns=["UserID"])
	return user_full.to_dict("records")

def rating(userID, BookID, Rating):
	updated = False
	with open('ml-latest-small/ratings.csv', 'r') as rf, open('ml-latest-small/temp.csv', 'w') as wf:
		for line in rf:
			line2 = (line.strip("\n")).split(",")
			#if line has data, and isnt just an empty line
			if(line2[0]!=''):
				#if userid and bookid match the rating on that line, we need to replace, not append
				if(int(line2[0])==userID and int(line2[1])==BookID):
					updated = True
					if(Rating>0):
						#if rating is 0, we dont replace with new rating, we skip
						wf.write('%s,%s,%s\n' % (userID, BookID, Rating))
				else:
					wf.write(line)
	if(updated): 
		#if we updated, we needed to rewrite old file with new data
		os.remove('ml-latest-small/ratings.csv')
		os.rename('ml-latest-small/temp.csv','ml-latest-small/ratings.csv')
	else:
		#if we didnt update, we just needed to append to old data
		with open('ml-latest-small/ratings.csv', 'a') as rf:
			rf.write('\n%s,%s,%s' % (userID, BookID, Rating))
			os.remove('ml-latest-small/temp.csv')

def recommend_books(userID, num_recommendations=5):
	ratings_list = [i.strip().split(",") for i in open('ml-latest-small/ratings.csv', 'r').readlines()]
	books_list = [i.strip().split(",") for i in open('ml-latest-small/books.csv', 'r').readlines()]

	ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'BookID', 'Rating'], dtype = int)
	books_df = pd.DataFrame(books_list, columns = ['BookID', 'Title', 'Genres'])

	books_df['BookID'] = books_df['BookID'].astype(int)
	ratings_df['BookID'] = ratings_df['BookID'].astype(int)
	ratings_df['UserID'] = ratings_df['UserID'].astype(int)
	ratings_df['Rating'] = ratings_df['Rating'].astype(float)
    #returns table with userID as rows, BookID as columns, and ratings as entries
	R_df = ratings_df.pivot(index = 'UserID', columns ='BookID', values ='Rating').fillna(0);
    #returns simple matrix of values without row or column names
	R = R_df.to_numpy()
    #returns mean of each row, so basically average rating for each user   
	user_ratings_mean = np.mean(R, axis = 1)
    #returns rating given by each user for each book without the bias associated with that user
	R_demeaned = R - user_ratings_mean.reshape(-1, 1)

    #figure out what this does!!
	from scipy.sparse.linalg import svds
	U, sigma, Vt = svds(R_demeaned, k = 50)

    #returns in diagonal matrix form
	sigma = np.diag(sigma)


	all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
	preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
    # Get and sort the user's predictions
	user_row_number = userID - 1 # UserID starts at 1, not 0
	sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the book information.
	user_data = ratings_df[ratings_df.UserID == (userID)]
	user_full = (user_data.merge(books_df, how = 'left', left_on = 'BookID', right_on = 'BookID').
                     sort_values(['Rating'], ascending=False)
                 )
    # Recommend the highest predicted rating books that the user hasn't seen yet.
	recommendations = (books_df[~books_df['BookID'].isin(user_full['BookID'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'BookID',
               right_on = 'BookID').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).iloc[:num_recommendations, :-1]
)
	return recommendations

print(recommend_books(10,5))
