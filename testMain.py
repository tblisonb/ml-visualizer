from parser import MlData


if __name__ == "__main__":
    ml = MlData()
    ml.parse_ml_csv_file("~/Downloads/round1.csv")
    print("\nget_songs()")
    print(ml.get_songs())
    print("\nget_submitters()")
    print(ml.get_submitters())
    print("\nget_votes_for_submitter()")
    print(ml.get_votes_for_submitter("Jacoby"))
