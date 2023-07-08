import pandas as pd


###############################################################################################################################
# class MlData()
#
#   Class representing Music League data, containing member functions for mapping vote and submission data to relevant
#   inputs.

class MlData:

    ### Member Functions ######################################################################################################

    def __init__(self):
        self.csv_data = []

    ###########################################################################################################################
    # function parse_ml_csv_file(filename)
    #
    #   Opens <filename> for reading, parsing the csv data into a dictionary based on the following format...
    #
    #   +----------------------+-----------+-------------+-------------+-----+-------------+------------+
    #   | Number of Submitters | 23        |             |             |     |             |            |
    #   +----------------------+-----------+-------------+-------------+-----+-------------+------------+
    #   | Song                 | Submitter | <person1>   | <person2>   | ... | <personN>   | Total      |
    #   | <song1>              | <person1> | <points1,1> | <points1,2> | ... | <points1,N> | <total1>   |
    #   | <song2>              | <person2> | <points2,1> | <points2,2> | ... | <points2,N> | <total2>   |
    #   | ...                  | ...       | ...         | ...         | ... | ...         | ...        |
    #   | <songN>              | <personN> | <pointsN,1> | <pointsN,2> | ... | <pointsN,N> | <totalN>   |
    #   |                      | Total     | <totalFix>  | <totalFix>  | ... | <totalFix>  | <sumTotal> |
    #   +----------------------+-----------+-------------+-------------+-----+-------------+------------+
    #
    #   Fields <pointsA,B> are the number of points that submitter B gave to submitter A's song. This should always be zero
    #   when A == B. Each row ends in a total, being the number of points that row's song was awarded. Each column also ends in
    #   a total; this is just for validating data entry as each total should add up to the net number of votes per person for
    #   that round (total == upvotes - downvotes). There may be instances where all of the <totalFix> fields do not equal each
    #   other if the point total per submitter was adjusted after the round started.
    #
    #   Arguments:
    #   - <filename> path to a csv file with the format as described here.
    #
    #   Returns:
    #   - none

    def parse_ml_csv_file(self, filename):
        self.csv_data = pd.read_csv(filename)
        print("Imported data from " + filename + "...")
        print(self.csv_data)

    ###########################################################################################################################
    # function get_songs()
    #
    #   Gets a list of songs in the dataset.

    def get_songs(self):
        return self.csv_data.iloc[1:-1, 0].tolist()

    ###########################################################################################################################
    # function get_submitters()
    #
    #   Gets a list of submitters' names in the dataset.

    def get_submitters(self):
        return self.csv_data.iloc[1:-1, 1].tolist()

    ###########################################################################################################################
    # function get_votes_for_submitter(submitter_name)
    #
    #   Gets a list of vote counts for a given user; maps 1 to 1 at each index to the list returned by get_submitters().

    def get_votes_for_submitter(self, submitter_name):
        submitter_row = self.csv_data.loc[self.csv_data.iloc[:, 1] == submitter_name]
        return submitter_row.iloc[:, 2:-1].iloc[0].tolist()
