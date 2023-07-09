from parser import MlParser
from analyzer import MlAnalyzer


if __name__ == "__main__":
    mp = MlParser()
    mp.parse_ml_csv_file("~/Downloads/round1-v2.csv")
    print("\nget_songs()")
    print(mp.get_songs())
    print("\nget_submitters()")
    print(mp.get_submitters())
    print("\nget_song_for_submitter()")
    print(mp.get_song_for_submitter("Jacoby"))
    print("\nget_submitter_for_song()")
    print(mp.get_submitter_for_song("Losing It"))
    print("\nget_submitter_votes_for_song()")
    print(mp.get_submitter_votes_for_song("Losing It"))
    print("\nget_song_votes_for_submitter()")
    print(mp.get_song_votes_for_submitter("Jacoby"))

    ma = MlAnalyzer(mp)
    # print("\ncalculate_similar_submitters()")
    # ma.calculate_similar_submitters("Jacoby")
