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
    # function get_df(round_number = None)
    #
    #   Gets the internal Dataframe.

    def get_df(self, round_number = None):
        if round_number is None:
            return self.df
        else:
            return self.df.loc[self.df["Round"] == round_number].iloc[:,1:]

    ###########################################################################################################################
    # function get_rounds(submitter_name = None)
    #
    #   Gets a list of rounds in the data set.

    def get_rounds(self, submitter_name = None):
        if submitter_name is None:
            seen = set()
            seen_add = seen.add
            return [x for x in self.df["Round"].tolist() if not (x in seen or seen_add(x))]
        else:
            return self.df.loc[self.df["Submitter"] == submitter_name]["Round"].tolist()

    ###########################################################################################################################
    # function get_songs(round_number = None, submitter_name = None)
    #
    #   Gets a list of songs for a given round <round_number> in the dataset.

    def get_songs(self, round_number = None, submitter_name = None):
        #   Error checking for arguments.
        if round_number is not None and (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        if submitter_name is not None and (len(self.df.loc[self.df["Submitter"] == submitter_name]) <= 0):
            print("Submitter \"" + str(submitter_name) + "\" does not exist.")
            return None
        #   Cases based on which arguments were provided.
        if round_number is None and submitter_name is None:
            return self.df["Song"].tolist()
        elif round_number is not None and submitter_name is None:
            return self.df["Song"].loc[self.df["Round"] == round_number].tolist()
        elif round_number is None and submitter_name is not None:
            return self.df.loc[self.df["Submitter"] == submitter_name]["Song"].tolist()
        else:
            submitter_row = self.df.loc[self.df["Submitter"] == submitter_name].loc[self.df["Round"] == round_number]
            if (len(submitter_row["Song"]) < 1):
                print("No submitter found for song \"" + song_name + "\" in round \"" + str(round_number) + "\".")
                return None
            return submitter_row["Song"].iloc[0]

    ###########################################################################################################################
    # function get_submitters(round_number = None, song_name = None)
    #
    #   Gets a list of submitters' names for a given round <round_number> in the dataset.

    def get_submitters(self, round_number = None, song_name = None):
        #   Error checking for arguments.
        if round_number is not None and (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        if song_name is not None and (len(self.df.loc[self.df["Song"] == song_name]) <= 0):
            print("Song \"" + str(song_name) + "\" does not exist.")
            return None
        #   Cases based on which arguments were provided.
        if round_number is None and song_name is None:
            return self.df.columns.values[3:].tolist()
        elif round_number is not None and song_name is None:
            return self.df["Submitter"].loc[self.df["Round"] == round_number].tolist()
        elif round_number is None and song_name is not None:
            return self.df.loc[self.df["Song"] == song_name]["Submitter"].tolist()
        else:
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

    ###########################################################################################################################
    # function get_total_points_for_submitter(submitter_name)
    #
    #   Gets the total number of points awarded to <submitter_name> for all rounds.

    def get_total_points_for_submitter(self, submitter_name):
        rounds = self.get_rounds(submitter_name=submitter_name)
        total = 0
        for round in rounds:
            song = self.get_songs(submitter_name=submitter_name, round_number=round)
            assert(isinstance(song, str))
            total += self.get_net_total_points_for_song(round, song)
        return total

    ###########################################################################################################################
    # function get_cumulative_points_awarded(round_number=None)
    #
    #   Gets a dataframe containing the total number of points awarded to each submitter by each submitter across all rounds up
    #   to <round_number> (all rounds in dataset if <round_number> is not specified).

    def get_cumulative_points_awarded(self, round_number=None):
        if round_number is not None and (len(self.df.loc[self.df["Round"] == round_number]) <= 0):
            print("Round number \"" + str(round_number) + "\" does not exist.")
            return None
        #   Exclude first two columns which aren't relevant for this function.
        if round_number is not None:
            round_subset_df = self.df.loc[self.df["Round"] <= round_number]
        else:
            round_subset_df = self.df
        all_submitters = self.get_submitters()
        agg_functions = dict(zip(all_submitters, ["sum"] * len(all_submitters)))
        return round_subset_df.groupby(round_subset_df["Submitter"], as_index=False).aggregate(agg_functions)

    ###########################################################################################################################
    # function get_bf_format()
    #
    #   Gets a specific string format for a "bar fight" visualization; data includes cumulative point totals per round for each
    #   submitter.

    def get_bf_format(self):
        result = "[\n"
        for round_number in self.get_rounds():
            round_df = self.get_cumulative_points_awarded(round_number=round_number)
            for person in self.get_submitters(round_number=round_number):
                points = str(sum(round_df.loc[round_df["Submitter"] == person].iloc[0, 1:].tolist()))
                result += "    {\"order\": " + str(round_number) + ", \"name\": \"" + person + "\", \"value\": " + points + "},\n"
        result += "]"
        return result
