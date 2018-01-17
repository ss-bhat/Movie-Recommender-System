# Movie-Recommender-System

Note: "All new ideas technisques for efficient codings are welcome." Thanks

This uses memory based collaborative filtering technique.

Collaborative Filtering:

* Data: ratings.txt is converted into user_id(index) and Movie_id(columns) table.

* From the user_movie table found the user user similarity matrix.

* Selected top k similar users i.e top k columns for a given user_id. Note: Here, k = 10 used. 
k value can be varied depending on importance of precision or recall.

* Both pearson correlation and cosine similarity is experimented and finally selected cosine similarity, because of its simplicty and quickness.

* For a given user id, ratings are predicted using the prediction formula.

* Movies with highest predicted ratings are recommended, for which the active user have not rated yet.

Popular/Top rated model:

* Arranged the movies in descending order according to the most number of user watched and the corresponding movie rating.

* Selected top n movies.

* Recommend those movies from top n for  which the active user have not seen the movie yet.

Areas of improvlment:

* Can combine machine learninbg techniques for personal profiling.

* Implementatipon of new user new item or movie

* SVD can be used to reduce sparse matrix.

* Can combine content based filtering to lalready existing one.

* Note: Update of User-Movie table takes lots of time nearly 30 minutes. If possible, this need to be reduced with efficipent coding.

* Or can be implemented in Apache Spark


Front End:

* Contains 3 pages, login page, home page and admin page.

* Login page contains list of test user ids and test password for testing purpose. pwd: 123Swaroop

* Home page, contains Top rated and Recommended movies for a given user id.

* Admin page can be used to update user movie table. Admin pwd:123Chopper
