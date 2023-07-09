from parser import MlParser


class MlAnalyzer:

    def __init__(self, parser):
        self.parser = parser

    def calculate_similar_submitters(self, submitter):
        submitters = self.parser.get_submitters()
        votes = [None] * len(submitters)
        submitter_votes = self.parser.get_votes_for_submitter(submitter)
        for i in range(len(submitters)):
            votes[i] = self.parser.get_votes_for_submitter(submitters[i])
        #   Data must be square.
        assert len(votes) == len(votes[0])
        net_diff = [None] * len(submitters)
        for i in range(len(votes)):
            for j in range(len(votes)):
                net_diff[i] += votes[j][i]
