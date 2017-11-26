import datetime

class VoterInfo(object):
    def __init__(self, name, voterID):
        self.name = name
        self.id = voterID


class ElectionDescr(object):
    def __init__(self, voters, polls_close):
        '''
        voters should be a collection of VoterInfo, and
        polls_close is a deadline after which voters are unable to vote
        polls_close is measured in seconds since the epoch, 01.01.1970 UTC time.
        '''
        self.voters = voters
        self.polls_close = polls_close


def SampleElection():
    '''
    Returns a sample election to be used for debugging, testing and prototyping.
    '''
    names = (
        'Alida Zurita',
        'Avril Eichenlaub',
        'Rozanne Brannum',
        'Wilhemina Nees',
        'Kina Hudnall',
        'Micha Soderlund',
        'Graig Granda',
        'Damien Edling',
        'Nam Stennis',
        'Ashly Torain',
    )
    voters = [ VoterInfo(name, i) for i, name in enumerate(names) ]
    polls_close = datetime.datetime(year=2017, month=11, day=28).timestamp()
    return ElectionDescr(voters, polls_close)
