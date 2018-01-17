def main(entered_user_id):
    import numpy as np
    import pandas as pd
    from sklearn.metrics.pairwise import pairwise_distances # This is used for cosine similarity.
    import glob2
    import os
    # import datetime
    from sklearn import cross_validation as cv

    class RecommendSystem:
        # Reading items file: This contains details about movie
        i_cols = ['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action',
                  'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                  'Film_Nair', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        items = pd.read_csv('u.item.txt', sep='|', names=i_cols, encoding='latin-1')
        items['release year'] = items["release date"].str.split('-').str[2]

        # Reading User files
        u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']

        users = pd.read_csv('u.user.txt', sep='|', names=u_cols, encoding='latin-1')

        # Splitting Test 25% and train data 75%
        test_data, train_data = \
            cv.train_test_split(pd.read_csv("u.data.txt", sep="\t",
                                            names=['User_id', 'Movie_id', 'Rating', 'Timestamp']),
                                test_size=0.25, random_state=100)

        def __init__(self, user_id):
            self.user_id = user_id
            self.user_movie_table = pd.read_csv(max(glob2.glob('*_User_Item_Table.csv'),
                                                    key=os.path.getctime), index_col=0)

            # pd.read_csv\
            # ("G:/Python/Recommender_sys_web/Demo/10-01-2018-20-35_User_Item_Table.csv", index_col=0)

        def popular_movies(self):
            """ Here top most popular movies is found by how many users have seen the movie and rated 5.
            Moreover, if we have a date of release for individual movies we can recommend the latest popular movies.
            This gives 10 most popular movies which is not seen by user.
            If user has already seen all the movies then, display random movies.
            """
            top_rated = RecommendSystem.train_data[RecommendSystem.train_data["Rating"] == 5]  # Top 5 rated movies

            # To get the most popular movies among the users
            pop_movies_id = list(top_rated.groupby('Movie_id').count()["Rating"].
                                 sort_values(ascending=False)[0:500].index)

            # The movies that are watched by users
            movies_id_watched_user = \
                list(RecommendSystem.train_data[RecommendSystem.train_data["User_id"] == int(self.user_id)].Movie_id)

            # The popular movies list that are not watched by user.
            rec_list = np.setdiff1d(pop_movies_id, movies_id_watched_user)

            # If all the popular movies are watched by user display repeated movies. Area of improvement.
            if len(rec_list) != 0:
                popular_mv = RecommendSystem.items[RecommendSystem.items["movie id"].
                    isin(rec_list)][["movie title"]][0:10]
            else:
                popular_mv = RecommendSystem.items.sample(n=50)[["movie title"]]

            return popular_mv

        def similar_users(self, k=10):
            """  This function is used to find the user-user similarity and cluster the most similar
            k( can used for tuning recall and precision) user. Here, cosine/Pearson similarity is used.
            Areas of improvement:
            New user
            New item
            This user_similarity_table can also be made as run in batch. i.e.
            Table gets updated at the end of the day.
            Note: Cosine Similarity is faster than pearson correlation.
            Pearson similarity gives better similarity value."""

            # Cosine Similarity
            # Converting data frame t numpy array for easier calculations.
            user_movie_matrix = self.user_movie_table.as_matrix()
            # User - user similarity (metric "cosine" used)
            user_similarity_matrix = pairwise_distances(user_movie_matrix, metric='cosine')
            # This give no of unique users as index. Used to create user - user similarity data frame
            sim_index = list(self.user_movie_table.index)
            # User user similarity data frame
            user_similarity_table = pd.DataFrame(user_similarity_matrix, index=sim_index, columns=sim_index)

            # Pearson Correlation for user user similarity
            # Transposing the table, where columns  = User_Id and rows = Movie_id
            #df_pearson = self.user_movie_table.T
            # Pearson correlation
            #correlation_table = df_pearson.corr(method='pearson')

            #user_similarity_table = correlation_table
            # Selecting top k similar users for a given user id.
            sim_user_id = dict(user_similarity_table.loc[int(self.user_id), ].sort_values(ascending=False)[0:k])

            # Storing User-User similar table
            # user_similarity_table.to_csv(datetime.datetime.now().
            # strftime("%d-%m-%Y-%H-%M" + "_user_user_similarity.csv"))

            # Returning k similar user default value is k = 10
            return sim_user_id

        def collaborative_filtering_predict(self, sim_user_id):

            """ Prediction of rating for a given user id using prediction formula.
            Areas of improvement: To show latest movies.
            Approach"""

            # Mean rating of the given user i.e. for user_id
            mean_rating = \
                self.user_movie_table.loc[int(self.user_id), ].sum() / len(self.user_movie_table.
                                                                           loc[int(self.user_id), ].nonzero()[0])

            # Sum of k neighbors similarity.
            denominator = sum(sim_user_id.values())

            # To operate only on those ratings given by user, to make calculation simpler replacing all 0 by NaN
            df = self.user_movie_table.loc[list(sim_user_id.keys()), ].replace(0, np.NaN)

            # Subtracting the user ratings with corresponding user mean.
            df = df.sub(df.mean(axis=1), axis=0)

            # Multiplying the above subtracted value with the corresponding user similarity.
            df = df.mul(list(sim_user_id.values()), axis=0)

            # Dividing the value by sum of k neighbors similarity.
            a = df.sum(axis=0) / denominator
            a = a.replace(0, np.NaN)
            s = a[a.notnull()].sort_values(ascending=False)

            # Predicted rating is the sum of mean user rating with the value obtained from above.
            predicted_rating = mean_rating + s

            # Retrieving the list of predicted rating and corresponding movie_id
            rec_mv_id = dict(predicted_rating)

            return rec_mv_id

        def recommendation(self, rec_mv_id):
            """ This function is used to recommend movies which are not seen by user.
            This is calculated by comparing the list of movies that are watched by user
            and list of movies recommended by
            collaborative filtering model. """

            # The below are the list of movies seen by user
            seen_mv = list(self.user_movie_table.loc[int(self.user_id), ][self.user_movie_table.loc[int(self.user_id), ]
                           .replace(0, np.NaN).notnull()].index)

            # This is the list of movies that can be recommended to a given user id
            rec_mv_id_lst = list(np.setdiff1d(np.array(list(rec_mv_id.keys())), np.array(seen_mv)))

            return rec_mv_id_lst

    # Asking user to enter the user id:

    # entered_user_id = int(input("Please enter a user id: "))

    # Creating an instance of class RecommendSystem
    ob_inst = RecommendSystem(entered_user_id)

    # Below if check if the user
    if entered_user_id in RecommendSystem.train_data.User_id.unique():

        # If for already existing user
        sim_users = ob_inst.similar_users()

        # Give recommendation.
        rec_mv_lst = ob_inst.collaborative_filtering_predict(sim_users)
        final_rec_mv_id_lst = ob_inst.recommendation(rec_mv_lst)

        """ Output:
            Popular Movies:
            Recommended Movies (user specific):
            Format: DataFrame."""

        top_rated_movies = ob_inst.popular_movies()

        reco_for_you = RecommendSystem.items[RecommendSystem.items["movie id"].
            isin(list(final_rec_mv_id_lst))][["movie title", "release date"]].iloc[0:10, ]

    else:
        # If its a new user give on popular movies.
        top_rated_movies = ob_inst.popular_movies()
        reco_for_you = "New_user"

    return top_rated_movies, reco_for_you
