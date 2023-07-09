import pandas as pd


###############################################################################################################################
# class MlParser()
#
#   Class representing Music League data, containing member functions for mapping vote and submission data to relevant inputs.

class MlParser:

    ### Member Functions ######################################################################################################

    def __init__(self):
        self.df = []

    ###########################################################################################################################
    # function parse_ml_csv_file(filename)
    #
    #   Opens <filename> for reading, parsing the csv data into a dictionary based on the following format...
    #
    #   +----------+---------+-----------+-------------+-------------+-----+-------------+
    #   | Round    | Song    | Submitter | <person1>   | <person2>   | ... | <personN>   |
    #   | <round1> | <song1> | <person1> | <points1,1> | <points1,2> | ... | <points1,N> |
    #   | <round1> | <song2> | <person2> | <points2,1> | <points2,2> | ... | <points2,N> |
    #   | ...      | ...     | ...       | ...         | ...         | ... | ...         |
    #   | <roundM> | <songN> | <personN> | <pointsN,1> | <pointsN,2> | ... | <pointsN,N> |
    #   +----------+---------+-----------+-------------+-------------+-----+-------------+
    #
    #   Fields <pointsA,B> are the number of points that submitter B gave to submitter A's song. This should always be zero
    #   when A == B.
    #
    #   Arguments:
    #   - <filename> path to a csv file with the format as described here.
    #
    #   Returns:
    #   - none

    def parse_ml_csv_file(self, filename):
        self.df = pd.read_csv(filename)

    ###########################################################################################################################
    # function get_df()
    #
    #   Gets the internal Dataframe.

    def get_df(self):
        return self.df

    ###########################################################################################################################
    # function get_df_for_round(round_number)
    #
    #   Gets the internal Dataframe for a give round.

    def get_df_for_round(self, round_number):
        return self.df.loc[self.df["Round"] == round_number]

    ###########################################################################################################################
    # function get_rounds()
    #
    #   Gets a list of rounds in the data set.

    def get_rounds(self):
        seen = set()
        seen_add = seen.add
        return [x for x in self.df["Round"].tolist() if not (x in seen or seen_add(x))]

    ###########################################################################################################################
    # function get_songs(round_number)
    #
    #   Gets a list of songs for a given round <round_number> in the dataset.

    def get_songs(self, round_number):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        return self.df["Song"].loc[self.df["Round"] == round_number].tolist()

    ###########################################################################################################################
    # function get_submitters(round_number)
    #
    #   Gets a list of submitters' names for a given round <round_number> in the dataset.

    def get_submitters(self, round_number):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        return self.df["Submitter"].loc[self.df["Round"] == round_number].tolist()

    ###########################################################################################################################
    # function get_song_for_submitter(round_number, submitter_name)
    #
    #   Gets the song associated with <submitter_name> for a given round <round_number>.

    def get_song_for_submitter(self, round_number, submitter_name):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        submitter_row = self.df.loc[self.df["Submitter"] == submitter_name].loc[self.df["Round"] == round_number]
        if (len(submitter_row["Song"]) < 1):
            print("No submitter found for song \"" + song_name + "\" in round \"" + str(round_number) + "\".")
            return None
        return submitter_row["Song"].iloc[0]

    ###########################################################################################################################
    # function get_submitter_for_song(round_number, song_name)
    #
    #   Gets the submitter associated with <song_name> for a given round <round_number>.

    def get_submitter_for_song(self, round_number, song_name):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        song_row = self.df.loc[self.df["Song"] == song_name].loc[self.df["Round"] == round_number]
        if (len(song_row["Submitter"]) < 1):
            print("No submitter found for song \"" + song_name + "\" in round \"" + str(round_number) + "\".")
            return None
        return song_row["Submitter"].iloc[0]

    ###########################################################################################################################
    # function get_submitter_votes_for_song(round_number, song_name)
    #
    #   Gets a dictionary of vote counts for a given song for a given round <round_number>; key = submitter, value = points.

    def get_submitter_votes_for_song(self, round_number, song_name):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        song_row = self.df.loc[self.df["Song"] == song_name].loc[self.df["Round"] == round_number]
        if (len(song_row["Song"]) < 1):
            print("Song \"" + song_name + "\" not found.")
            return None
        #   The first three columns are not point data so ignore them.
        all_submitters_dict = song_row.iloc[0, 3:].to_dict()
        #   Filter dict based on who was actually participating in the round <round_number>.
        return {key: all_submitters_dict[key] for key in self.get_submitters(round_number)}

    ###########################################################################################################################
    # function get_song_votes_for_submitter(round_number, submitter_name)
    #
    #   Gets a dictionary of vote counts for a given submitter for a given round <round_number>; key = song, value = points.

    def get_song_votes_for_submitter(self, round_number, submitter_name):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        if (submitter_name not in self.df.loc[self.df["Round"] == round_number]):
            print("Submitter \"" + submitter_name + "\" not found in round \"" + str(round_number) + "\".")
            return None
        submitter_col = self.df[submitter_name].loc[self.df["Round"] == round_number]
        #   Create a dictionary of two different lists; being the songs and the points awarded by <submitter_name>.
        return dict(zip(self.get_songs(round_number), submitter_col))

    ###########################################################################################################################
    # function get_net_total_points_for_song(round_number, song_name)
    #
    #   Gets the total number of points awarded to <song_name> by all submitters for a given round <round_number>.

    def get_net_total_points_for_song(self, round_number, song_name):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        song_row = self.df.loc[self.df["Song"] == song_name].loc[self.df["Round"] == round_number]
        if (len(song_row["Song"]) < 1):
            print("Song \"" + song_name + "\" not found.")
            return None
        #   The first three columns are not point data so ignore them.
        return sum(song_row.iloc[0, 3:].tolist())

    ###########################################################################################################################
    # function get_absolute_total_points_for_submitter(round_number, submitter_name)
    #
    #   Gets the absolute total number of points awarded by <submitter_name> for all songs for a given round <round_number>
    #   (meaning all votes positive and negative are counted).

    def get_absolute_total_points_for_submitter(self, round_number, submitter_name):
        if (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        if (submitter_name not in self.df):
            print("Submitter \"" + submitter_name + "\" not found.")
            return None
        submitter_col = self.df[submitter_name].loc[self.df["Round"] == round_number]
        return sum(map(abs, submitter_col))