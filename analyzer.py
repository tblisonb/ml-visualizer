class MlAnalyzer:

    def __init__(self, parser):
        self.parser = parser

    def calculate_similar_submitters_for_round(self, round_number, submitter_name):
        #   If <submitter_name> did not vote in the round, there's nothing to do.
        if (self.parser.get_absolute_total_points_for_submitter(round_number, submitter_name) == 0):
            print("Submitter \"" + submitter_name + "\" did not vote in round \"" + str(round_number) + "\".")
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
        submitters.remove(submitter_name)
        aggregate_dict = {person: [] for person in submitters}
        for round in rounds:
            similar_votes = self.calculate_similar_submitters_for_round(round, submitter_name)
            #   If <similar_votes> is None, then that person submitted but did not vote in round <round>, so we skip it.
            if similar_votes is None:
                continue
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
        sum_df = self.parser.get_cumulative_points_awarded()
        submitters = self.parser.get_submitters()
        votes_to_list = sum_df[submitter_name].tolist()
        votes_from_list = sum_df.loc[sum_df["Submitter"] == submitter_name].iloc[:, 1:].iloc[0].tolist()
        #   Need to remove the submitter we're getting info on from these lists as it doesn't make sense if they come up here
        # (i.e. PersonA gave the least points to PersonA).
        self_idx = submitters.index(submitter_name)
        del votes_to_list[self_idx]
        del votes_from_list[self_idx]
        del submitters[self_idx]
        print("Gave the most points to " + str(submitters[votes_to_list.index(max(votes_to_list))]) + " (" + str(max(votes_to_list)) + ").")
        print("Gave the least points to " + str(submitters[votes_to_list.index(min(votes_to_list))]) + " (" + str(min(votes_to_list)) + ").")
        print("Received the most points from " + str(submitters[votes_from_list.index(max(votes_from_list))]) + " (" + str(max(votes_from_list)) + ").")
        print("Received the least points from " + str(submitters[votes_from_list.index(min(votes_from_list))]) + " (" + str(min(votes_from_list)) + ").")
        print("How they voted compared to other participants...")
        print("  Most Similar - ")
        for entry in similar_list[::-1][:3]:
            print("    " + entry[0] + 
              " had " + "{0:.0%}".format(entry[1]) + 
              " overlap across " + str(entry[2]) + " mutual round(s).")
        print("  Least Similar - ")
        for entry in similar_list[:3]:
            print("    " + entry[0] + 
              " had " + "{0:.0%}".format(entry[1]) + 
              " overlap across " + str(entry[2]) + " mutual round(s).")
        max_value = 0.0
        min_value = 100.0
        for round_num in rounds:
            similar_list = self.calculate_similar_submitters_for_round(round_num, submitter_name)
            if similar_list is None:
                continue
            for person in similar_list:
                if similar_list[person] > max_value:
                    max_value = similar_list[person]
                    max_person = person
                    max_round_num = round_num
                if similar_list[person] < min_value:
                    min_value = similar_list[person]
                    min_person = person
                    min_round_num = round_num
        print("Highest voting overlap for a single round was in round number " + str(max_round_num) + ": " + max_person + " with " + "{0:.0%}".format(max_value) + " overlap.")
        print("Lowest voting overlap for a single round was in round number " + str(min_round_num) + ": " + min_person + " with " + "{0:.0%}".format(min_value) + " overlap.")