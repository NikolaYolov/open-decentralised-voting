import hashlib
import pickle
import numpy as np
from const import const_modulo, const_power
import random
random.seed(20171125)


def compute_hash(parentHash, number, content):
    to_hash = pickle.dumps((parentHash, number, content, const_modulo))
    return hashlib.sha256(to_hash).hexdigest()


def encrypt(n):
    #return const_power**n % const_modulo
    return n



class Block(object):
    """
    #Description:
    Block of a blockchain.

    #Variables:
    parentHash : 
    blockHash : 
    number : 
    content : dictionary of (i,j) : phi(a_ij)

    #Methods:
    is_valid() : 
    """
    def __init__(self, parentHash, blockHash, number, content):
        self.parentHash = parentHash
        self.blockHash = blockHash
        self.number = number
        self.content = content


    def is_valid_hash(self):
        """
        Assert the validity of a block: if its content is valid, and if its hash matches its content and parentHash.
        """
        pickled_content = self.content#pickle!
        if self.blockHash != compute_hash(self.parentHash, self.number, self.content):
            Exception('Block hash incorrect, it is %s'%self.blockHash)
            return False
        else:
            return True
    

    def make_dummy(self):
        voter = random.randint(0, 19)
        self.content = {
            (voter, i) : random.randint(0, 3570381) for i in range(20)
        }
        self.parentHash = 'GENESIS'
        self.number = 1
        self.blockHash = compute_hash(self.parentHash, self.number, self.content)


class Blockchain(object):
    """
    name : string
    chain : dictionary of hashes & Blocks
    headers : list of hashes that are heads of the blockchain tree
    superheaders : list of hashes that are heads of the superblocks in the blockchain tree
    """
    def __init__(self, name, voterIDs):
        self.name = name
        self.voterIDs = voterIDs
        self.genesisHash = compute_hash(None, 0, {})
        genesis_block = Block(
            parentHash=None, 
            blockHash=self.genesisHash, 
            number=0, 
            content={}
        )
        self.chain = {
            self.genesisHash : genesis_block
        }
        self.headers = [self.genesisHash]
        self.superheaders = []


    def determine_latestHash(self, is_superblock=False):
        """
        Determine head of the longest chain, resolving ties lexicographically through hashes.
        """
        running_max = 0
        latestHash = self.genesisHash
        if not is_superblock:
            headers = sorted(self.headers)
        else:
            if self.superheaders == []:
                self.superheaders = [self.determine_latestHash()]
            headers = sorted(self.superheaders)
        for header in headers:
            number = self.chain[header].number
            if number > running_max:
                running_max = number
                latestHash = header
        return latestHash


    def longest_chain(self):
        """
        Determine longest blockchain by retrieving ancestors of latestHash.
        """
        latestHash = self.determine_latestHash()
        long_chain = {
            self.genesisHash : self.chain[self.genesisHash]
        }
        while latestHash != self.genesisHash:
            latestBlock = self.chain[latestHash]
            long_chain[latestHash] = latestBlock
            latestHash = latestBlock.parentHash
        return long_chain


    def construct_state(self):
        """
        Determine matrix of tinyVotes from longest chain.
        """
        state = {}
        long_chain = self.longest_chain()
        blocks = long_chain.values()
        for block in blocks:
            content = block.content
            for key in content.keys():
                if key in state.keys():
                    Exception(str(key)+' appears multiple times in chain!')
                state[key] = content[key]
        return state


    def construct_substate(self, block):
        """
        Determine matrix of tinyVotes from ancestors of block.
        """
        substate = {}
        while block.parentHash != self.genesisHash:
            block = self.chain[block.parentHash]
            content = block.content
            for key in content.keys():
                if key in substate.keys():
                    Exception(str(key)+' appears multiple times in chain!')
                substate[key] = content[key]
        return substate


    def construct_superstate(self):
        """
        Determine list of superblock rowsums from longest chain.
        """
        state = {}
        latestHash = self.determine_latestHash(is_superblock=True)
        block = self.chain[latestHash]
        blockHash = block.blockHash
        while blockHash != self.genesisHash:
            parentHash = block.parentHash
            content = block.content
            for key in content.keys():
                if key in state.keys():
                    Exception(str(key)+' appears multiple times in chain!')
                if type(key) == tuple:
                    break
                state[key] = content[key]
            block = self.chain[parentHash]
            blockHash = block.blockHash
        return state


    def has_voted(self):
        state = self.construct_state()        
        return {[key[0] for key in state.keys()]}


    def is_complete_state(self):
        """
        Determine whether all votes have been cast.
        """
        state = self.construct_state()
        state_keys = sorted(state.keys())
        all_keys = [[(i, j) for j in self.voterIDs if i != j] for i in self.voterIDs]
        all_keys = sorted([key for sublist in all_keys for key in sublist])
        return state_keys == all_keys


    def is_finished(self):
        """
        Determine whether all votes have been cast and verified.
        """
        is_complete_state = self.is_complete_state()
        is_complete_superstate = sorted(self.construct_superstate().keys()) == sorted(self.voterIDs)
        return is_complete_state & is_complete_superstate


    def is_valid_vote(self, block, is_new_block=True):
        """
        Check that:
        - tinyVotes have not been cast yet in the longest chain
        - all tinyVotes of voter are cast exactly once to all other voters
        """
        if is_new_block:
            state = self.construct_state()
        else:
            state = self.construct_substate(block)
        used_keys = state.keys()
        new_keys = block.content.keys()
        intersect = set(used_keys) & set(new_keys)
        is_new = intersect == set()

        new_voters = set([key[0] for key in new_keys])
        is_complete = True
        for new_voter in new_voters:
            votees = [key[1] for key in new_keys if key[0] == new_voter]
            other_voters = [vid for vid in self.voterIDs if vid != new_voter]
            is_complete *= sorted(votees) == sorted(other_voters)
        return is_complete & is_new


    def is_valid_row(self, content, is_new_block=True):
        """
        For superblocks, verify that row sum of encrypted tinyVotes equals content of superblock, 
        and rowsum has not been given before. 
        """
        assert self.is_complete_state()
        state = self.construct_state()
        for key in content.keys():
            if key in self.construct_superstate().keys():
                raise Exception('Sum of tinyVotes already in blockchain!')               
            sum_tinyVotes = np.sum([state[(i, key)] for i in self.voterIDs if i != key])
            encrypted_rowsum = encrypt(content[key])
            if not sum_tinyVotes == encrypted_rowsum:
                raise Exception('Sum of tinyVotes does not equal encrypted sum of row %s'%str(key))
        return True


    def is_valid_block(self, parentHash, block, is_new_block=True, is_superblock=False):
        """
        For normal blocks, checks:
        - correctness of block's hash
        - accuracy of block's parent hash
        - accuracy of block's number
        - validity of contents of block

        For superblocks, also:
        - check everyone has voted
        - verify blockchain of normal blocks
        """
        parentNumber = self.chain[parentHash].number
        blockNumber = block.number
        if not block.is_valid_hash():
            raise Exception('Invalid hash of block %s'%blockNumber)
        elif block.parentHash != parentHash:
            raise Exception('Parent hash not accurate at block %s'%blockNumber)
        elif blockNumber != parentNumber + 1:
            raise Exception('Number not accurate at block %s'%blockNumber)

        if not is_superblock:
            if not self.is_valid_vote(block, is_new_block=is_new_block):
                raise Exception('Invalid content of block %s'%blockNumber)
        else:
            if not self.is_complete_state():
                not_voted = [vid for vid in self.voterIDs if vid not in self.has_voted()]
                raise Exception('Voting has not been completed yet! To vote: %s'%str(not_voted))            
            self.verify()
            if not self.is_valid_row(block.content, is_new_block=True):
                raise Exception('Invalid content of block %s'%blockNumber)

        return True


    def add_block(self, content, is_superblock=False):
        """
        Construct new (super)block from content, check whether it is valid and add under appropriate parent. 
        Then update (super)headers.
        """
        if not is_superblock:
            parentHash = self.determine_latestHash()
        else:
            parentHash = self.determine_latestHash(is_superblock=True)
        number = self.chain[parentHash].number + 1
        blockHash = compute_hash(parentHash, number, content)
        block = Block(
            parentHash=parentHash, 
            blockHash=blockHash, 
            number=number, 
            content=content
        )

        if not self.is_valid_block(parentHash, block, is_superblock=is_superblock):
            assert Exception('Oh no, invalid block!')
        
        self.chain[blockHash] = block

        if not is_superblock:
            self.headers.remove(parentHash)
            self.headers.append(blockHash)
        else:
            self.superheaders.remove(parentHash)
            self.superheaders.append(blockHash)

        print('Block added, new length of blockchain: %d'%number)


    def verify(self):
        """
        Verify all blocks in the entire blockchain (also those not in the longest chain).
        """
        for header in self.headers:
            block = self.chain[header]
            parentHash = block.parentHash
            blockHash = block.blockHash
            while parentHash != None:
                if not self.is_valid_block(parentHash, block, is_new_block=False):
                    Exception('Header with hash %s is not valid!'%blockHash)
                block = self.chain[parentHash]
                parentHash = block.parentHash
                blockHash = block.blockHash
            assert blockHash == self.genesisHash
        return True


    def print_chain(self):
        headers = self.superheaders + self.headers
        seen = []
        for header in headers:
            if header in seen:
                continue
            print('Printing everything below header %s'%header)
            block = self.chain[header]
            content = block.content
            blockHash = block.blockHash
            while blockHash != self.genesisHash:
                parentHash = block.parentHash
                content = block.content
                #if not self.is_valid_block(parentHash, block):
                #    Exception('Header with hash %s is not valid!'%blockHash)
                #else:
                print('  >>block number %d'%block.number)
                print('    parentHash: %s'%parentHash)
                print('    blockHash: %s'%blockHash)
                print('    contents:')
                for key in content.keys():
                    print('        %s : %d'%(str(key), content[key]))
                print('\n')
                block = self.chain[parentHash]
                if blockHash in headers:
                    seen.append(blockHash)
                blockHash = parentHash
            print('  >>Genesis block reached\n')


    def merge(self, blockchain):
        """
        Merge two blockchains.
        """
        other_chain = blockchain.chain
        for other_key, other_block in other_chain.items():
            if other_key not in self.chain:
                self.chain[other_key] = other_block

                other_blockHash = other_block.blockHash
                other_parentHash = other_block.parentHash
                if other_parentHash in self.headers:
                    self.headers.remove(other_parentHash)
                    self.headers.append(other_blockHash)
                elif other_parentHash in self.superheaders:
                    self.superheaders.remove(other_parentHash)
                    self.superheaders.append(other_blockHash)

        for header in blockchain.headers:
            if header not in self.headers:
                self.headers.append(header)
        for header in blockchain.superheaders:
            if header not in self.superheaders:
                self.superheaders.append(header)



def make_full_votes():
    b = Blockchain('test', range(10))
    for j in b.voterIDs:
        #content = {(j, i) : random.randint(3285625, 328562583) for i in b.voterIDs if i != j}
        content = {(j, i) : 1 for i in b.voterIDs if i != j}
        b.add_block(content)
    
        if j == 1:
            parentHash = b.headers[0]

    #content = {(3, i) : random.randint(3285625, 23593845230467) for i in range(10) if i != j}
    content = {(3, i) : 1 for i in range(10) if i != 3}
    blockHash = compute_hash(parentHash, 3, content)
    conflict_block = Block(
        parentHash=parentHash, 
        blockHash=blockHash, 
        number=3, 
        content=content
    )
    b.headers.append(blockHash)
    b.chain[blockHash] = conflict_block
    
    return b


def make_short_votes1():
    b = Blockchain('test', range(10))
    for j in range(2):
        #content = {(j, i) : random.randint(3285625, 328562583) for i in b.voterIDs if i != j}
        content = {(j, i) : 1 for i in b.voterIDs if i != j}
        b.add_block(content)
    
        if j == 1:
            parentHash = b.headers[0]

    #content = {(3, i) : random.randint(3285625, 23593845230467) for i in range(10) if i != j}
    content = {(3, i) : 1 for i in range(10) if i != j}
    blockHash = compute_hash(parentHash, 3, content)
    conflict_block = Block(
        parentHash=parentHash, 
        blockHash=blockHash, 
        number=3, 
        content=content
    )
    b.headers.append(blockHash)
    b.chain[blockHash] = conflict_block
    
    return b


def make_short_votes2():
    b = Blockchain('test', range(10))
    for j in range(5,8):
        #content = {(j, i) : random.randint(3285625, 328562583) for i in b.voterIDs if i != j}
        content = {(j, i) : 1 for i in b.voterIDs if i != j}
        b.add_block(content)
    
        if j == 1:
            parentHash = b.headers[0]    
    return b



def make_full_superstate(b):
    for j in b.voterIDs:
        #content = {(j, i) : random.randint(3285625, 328562583) for i in b.voterIDs}
        content = {j : 9 for i in b.voterIDs}
        b.add_block(content, is_superblock=True)


"""
PROTOCOL:

while not finished:
    #broadcast blockchain
    #receive blockchain
    #verify
    while not self.is_complete():
        #if own tinyVotes not in longest chain: mine own tinyVotes
        #broadcast blockchain

    if self.is_complete():
        #if own superblock not in longest chain: mine superblock
        #broadcast blockchain
"""



