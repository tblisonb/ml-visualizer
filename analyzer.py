class MlAnalyzer:

    def __init__(self, parser):
        self.parser = parser

    def calculate_similar_submitters_for_round(self, round_number, submitter_name):
        #   If <submitter_name> did not vote in the round, there's nothing to do.
        if (self.parser.get_absolute_total_points_for_submitter(round_number, submitter_name) == 0):
            print("Submitter \"" + submitter_name + "\" did not vote in this round.")
            return
        submitters = self.parser.get_submitters(round_number)
        submitter_votes = self.parser.get_song_votes_for_submitter(round_number, submitter_name)
        submitter_vote_total = 0
        net_diff = dict(zip(submitters, [0] * len(submitters)))
        for person in submitters:
            compare_votes = self.parser.get_song_votes_for_submitter(round_number, person)
            assert(len(submitter_votes) == len(compare_votes))
            #   <vote> should be a key,value pair where the key is the song name and the value is the number of points.
            for song in submitter_votes:
                net_diff[person] += abs(submitter_votes[song] - compare_votes[song])
        #   Remove key,value pair for <submitter_name> as it's always zero since it's comparing the person to themself.
        del net_diff[submitter_name]
        adjusted_dict = dict.fromkeys(net_diff.keys())
        for key in net_diff:
            adjusted_dict[key] = 1 - (net_diff[key] / (2 * self.parser.get_absolute_total_points_for_submitter(round_number, submitter_name)))
        return adjusted_dict

    def calculate_similar_submitters(self, submitter_name):
        rounds = self.parser.get_rounds(submitter_name=submitter_name)
        submitters = self.parser.get_submitters()
        aggregate_dict = {person: [] for person in submitters}
        for round in rounds:
            similar_votes = self.calculate_similar_submitters_for_round(round, submitter_name)
            for person in similar_votes:
                aggregate_dict[person].append(similar_votes[person])
        average_list = []
        for person in aggregate_dict:
            if len(aggregate_dict[person]) <= 0:
                continue
            average_list.append((person, sum(aggregate_dict[person]) / len(aggregate_dict[person]), len(aggregate_dict[person])))
        return sorted(average_list, key=lambda tup: tup[1])

    def get_formatted_metrics_for_submitter(self, submitter_name):
        rounds = self.parser.get_rounds(submitter_name=submitter_name)
        points = self.parser.get_total_points_for_submitter(submitter_name)
        similar_list = self.calculate_similar_submitters(submitter_name)
        assert(len(similar_list) > 1)
        print("--- Music League: Stats for " + submitter_name + " ---")
        print("Participated in " + str(len(rounds)) + " rounds.")
        print("Received " + str(points) + " points.")
        sum_df = self.parser.get_total_points_awarded()
        submitters = self.parser.get_submitters()
        row = sum_df[submitter_name]
        vote_list = row.tolist()
        print("Gave the most points to " + str(submitters[vote_list.index(max(vote_list))]) + " (" + str(max(vote_list)) + ").")
        print("Gave the least points to " + str(submitters[vote_list.index(min(vote_list))]) + " (" + str(min(vote_list)) + ").")
        print("How they voted compared to other participants...")
        for entry in reversed(similar_list):
            print("    " + entry[0] + 
              " had " + "{0:.0%}".format(entry[1]) + 
              " overlap across " + str(entry[2]) + " mutual round(s).")
        # print("Voted most similarly to " + similar_list[len(similar_list) - 1][0] + 
        #       " (with " + "{0:.0%}".format(similar_list[len(similar_list) - 1][1]) + 
        #       " overlap and " + str(similar_list[len(similar_list) - 1][2]) + " mutual round(s)).")
        # if (len(similar_list) >= 2):
        #     print("Runner up is " + similar_list[len(similar_list) - 2][0] + 
        #           " (with " + "{0:.0%}".format(similar_list[len(similar_list) - 2][1]) + 
        #           " overlap and " + str(similar_list[len(similar_list) - 2][2]) + " mutual round(s)).")
        # print("Voted least similarly to " + similar_list[0][0] + 
        #       " (with " + "{0:.0%}".format(similar_list[0][1]) + 
        #       " overlap and " + str(similar_list[0][2]) + " mutual round(s)).")
