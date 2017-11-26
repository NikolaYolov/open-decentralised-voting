import random
import const

class VoteMgr(object):
    def __init__(self, my_id, voter_ids):
        self.voted = False
        self.my_id = my_id
        self.voter_ids = voter_ids
        self.received_tiny_votes = {}

    def hasVoted(self):
        return self.voted

    def registerVote(self, vote):
        self.voted = True
        self.private_vote = random.randint(0, const.max_secret) * const.vote_separator
        + vote

        self.parts = {}
        left = self.private_vote
        ids_list = [vid for vid in self.voter_ids if vid != self.my_id]
        last_id = ids_list.pop()
        for vid in ids_list:
            self.parts[vid] = random.randint(0, self.private_vote)
            left -= self.parts[vid]
        self.parts[last_id] = left

    def getTinyVote(self, vid):
        return self.parts[vid]


    def registerTinyVote(self, vid, tiny_vote):
        self.received_tiny_votes[vid] = tiny_vote

    def tinyVotesCollected(self):
        return len(received_tiny_votes) == len(voter_ids) - 1

    def tinyVotesAggregation(self):
        assert self.tinyVotesCollected()
        return sum(received_tiny_votes.values())

