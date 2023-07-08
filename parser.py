import pandas as pd


###############################################################################################################################
# parse_ml_csv_file()
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
#   Fields <pointsA,B> are the number of points that submitter B gave to submitter A's song. This should always be zero when
#   A == B. Each row ends in a total, being the number of points that row's song was awarded. Each column also ends in a total;
#   this is just for validating data entry as each total should add up to the net number of votes per person for that round
#   (total == upvotes - downvotes). There may be instances where all of the <totalFix> fields do not equal each other if the
#   point total per submitter was adjusted after the round started.

def parse_ml_csv_file(filename):
    csv_data = pd.read_csv(filename)
    print(csv_data)

if __name__ == "__main__":
    parse_ml_csv_file("~/Downloads/round1.csv")
