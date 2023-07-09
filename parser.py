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
    #   +----------------------+-----------+-------------+-------------+-----+-------------+
    #   | Song                 | Submitter | <person1>   | <person2>   | ... | <personN>   |
    #   | <song1>              | <person1> | <points1,1> | <points1,2> | ... | <points1,N> |
    #   | <song2>              | <person2> | <points2,1> | <points2,2> | ... | <points2,N> |
    #   | ...                  | ...       | ...         | ...         | ... | ...         |
    #   | <songN>              | <personN> | <pointsN,1> | <pointsN,2> | ... | <pointsN,N> |
    #   +----------------------+-----------+-------------+-------------+-----+-------------+
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
        print("Imported data from " + filename + "...")
        print(self.df)

    ###########################################################################################################################
    # function get_songs()
    #
    #   Gets a list of songs in the dataset.

    def get_songs(self):
        return self.df["Song"].tolist()

    ###########################################################################################################################
    # function get_submitters()
    #
    #   Gets a list of submitters' names in the dataset.

    def get_submitters(self):
        return self.df["Submitter"].tolist()

    ###########################################################################################################################
    # function get_song_for_submitter(submitter_name)
    #
    #   Gets the song associated with <submitter_name>.

    def get_song_for_submitter(self, submitter_name):
        submitter_row = self.df.loc[self.df["Submitter"] == submitter_name]
        if (len(submitter_row["Song"]) < 1):
            print("No song found for submitter \"" + submitter_name + "\".")
            return None
        return submitter_row["Song"].iloc[0]

    ###########################################################################################################################
    # function get_submitter_for_song(song_name)
    #
    #   Gets the submitter associated with <song_name>.

    def get_submitter_for_song(self, song_name):
        song_row = self.df.loc[self.df["Song"] == song_name]
        if (len(song_row["Submitter"]) < 1):
            print("No submitter found for song \"" + song_name + "\".")
            return None
        return song_row["Submitter"].iloc[0]

    ###########################################################################################################################
    # function get_submitter_votes_for_song(song_name)
    #
    #   Gets a dictionary of vote counts for a given song; key = submitter, value = points.

    def get_submitter_votes_for_song(self, song_name):
        song_row = self.df.loc[self.df["Song"] == song_name]
        if (len(song_row["Song"]) < 1):
            print("Song \"" + song_name + "\" not found.")
            return None
        #   The first two columns are not point data so ignore them.
        return song_row.iloc[0, 2:].to_dict()

    ###########################################################################################################################
    # function get_song_votes_for_submitter(submitter_name)
    #
    #   Gets a dictionary of vote counts for a given submitter; key = song, value = points.

    def get_song_votes_for_submitter(self, submitter_name):
        if (submitter_name not in self.df):
            print("Submitter \"" + submitter_name + "\" not found.")
            return None
        submitter_col = self.df[submitter_name]
        #   Create a dictionary of two different lists; being the songs and the points awarded by <submitter_name> (these 
        # should always line up 1:1 assuming the data is square).
        return dict(zip(self.get_songs(), submitter_col))

    ###########################################################################################################################
    # function get_net_total_points_for_song(song_name)
    #
    #   Gets the total number of points awarded to <song_name> by all submitters.

    def get_net_total_points_for_song(self, song_name):
        song_row = self.df.loc[self.df["Song"] == song_name]
        if (len(song_row["Song"]) < 1):
            print("Song \"" + song_name + "\" not found.")
            return None
        #   The first two columns are not point data so ignore them.
        return sum(song_row.iloc[0, 2:].tolist())

    ###########################################################################################################################
    # function get_absolute_total_points_for_submitter(submitter_name)
    #
    #   Gets the absolute total number of points awarded by <submitter_name> for all songs (meaning all votes positive and
    #   negative are counted).

    def get_absolute_total_points_for_submitter(self, submitter_name):
        if (submitter_name not in self.df):
            print("Submitter \"" + submitter_name + "\" not found.")
            return None
        submitter_col = self.df[submitter_name]
        return sum(map(abs, submitter_col))