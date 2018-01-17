def main():

    """ This program is to update user_id and Movie_id table. This takes approximately 0:32:59.678982 minutes to run."""

    import pandas as pd
    from sklearn import cross_validation as cv
    import datetime

    class UserItemTable:

        # Class Variables
        # Reading ratings file: This contains user_id, movie_id and its ratings

        ratings = pd.read_csv("u.data.txt", sep="\t", names=['User_id', 'Movie_id', 'Rating', 'Timestamp'])

        # Splitting Test 25% and train data 75%
        test_data, train_data = cv.train_test_split(ratings, test_size=0.25, random_state=100)

        def __init__(self, date_time):
            self.date_time = date_time

        def user_item_data_frame(self):  # Returns user_movie table

            mv_id_clm = list(UserItemTable.train_data.Movie_id.unique())

            user_id_row = list(UserItemTable.train_data.User_id.unique())

            user_movie_table = pd.DataFrame(index=user_id_row, columns=mv_id_clm)

            for line in UserItemTable.train_data.itertuples():
                user_movie_table.loc[line[1], line[2]] = line[3]

            user_movie_table = user_movie_table.fillna(0)
            # All nan values are replaced with 0. Same is exported as csv file.

            user_movie_table.to_csv(self.date_time)

            return True

        @staticmethod
        def data():
            return UserItemTable.train_data

    try:
        start_time = datetime.datetime.now()

        update_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M" + "_User_Item_Table.csv")

        ob_class = UserItemTable(update_time)

        if ob_class.user_item_data_frame():

            end_time = datetime.datetime.now()

            message = "Table Updated Successfully"

            duration = end_time - start_time

            return message, duration

    except Exception as e:

        message = e
