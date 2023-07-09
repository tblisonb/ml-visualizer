class MlAnalyzer:

    def __init__(self, parser):
        self.parser = parser

    def calculate_similar_submitters(self, submitter_name):
        #   If <submitter_name> did not vote in the round, there's nothing to do.
        if (self.parser.get_absolute_total_points_for_submitter(submitter_name) == 0):
            print("Submitter \"" + submitter_name + "\" did not vote in this round.")
            return
        submitters = self.parser.get_submitters()
        submitter_votes = self.parser.get_song_votes_for_submitter(submitter_name)
        submitter_vote_total = 0
        net_diff = dict(zip(submitters, [0] * len(submitters)))
        for person in submitters:
            compare_votes = self.parser.get_song_votes_for_submitter(person)
            assert(len(submitter_votes) == len(compare_votes))
            #   <vote> should be a key,value pair where the key is the song name and the value is the number of points.
            for song in submitter_votes:
                net_diff[person] += abs(submitter_votes[song] - compare_votes[song])
        #   Remove key,value pair for <submitter_name> as it's always zero since it's comparing the person to themself.
        del net_diff[submitter_name]
        sorted_list = sorted(net_diff.items(), key=lambda item: item[1])
        adjusted_list = []
        for pair in sorted_list:
            adjusted_list.append((pair[0], 1 - (pair[1] / (2 * self.parser.get_absolute_total_points_for_submitter(submitter_name)))))
        return adjusted_list
