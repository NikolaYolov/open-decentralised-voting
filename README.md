# Decentralised anonymous voting

#### TL;DR

We construct, all from scratch, a blockchain, encryption method, peer-to-peer network and GUI for carrying out a completely decentralised, anonymous and resilient voting system.


### Motivation

We aim to learn how to develop a custom, purpose-built blockchain technology with an incorporated encryption using homomorphic functions. While we apply this to a voting system, this can be fairly easily be extended to any anonymous collective decision making process, such as auctions, the sharing of opinions or sensitive data (e.g.~medical records), donations, etc.


### Description

#### Blockchain
We build a blockchain in Python that contains two types of blocks. The procedure for voting is as follows:

1. The voter decides their vote $v_i$, which we may assume to be binary. They randomly construct some `tinyVotes' $a_{ij}$ with the property that $\sum_{j} a_{ij} = v_i$, where each $a_{ij}$ will be broadcast to voter $j$.
2. The voter encrypts their vote using a homomorphic (i.e.~`special') function $\phi$ and their private key $p_i$ and a public key $P$.
They mine all of these values $\phi (a_{ij})$ into the blockchain, which is regularly being broadcast and received through a peer-to-peer network. 
For resolving conflicts, we apply the longest chain rule.
3. When all votes have been cast, the blockchain will effectively contain a matrix of encrypted tinyVotes $\big( \phi (a_{ij}) \big)_{ij}$. Each user $i$ will also have received tinyVotes $a_{ji}$ from each voter $j \neq i$, from which they compute
$$
\sum_{j \neq i} a_{ji}.
$$
This value can be verified using the encrypted tinyVotes, since we have the relation
$$
\sum \phi (a_{ij}) = \phi\left( sum_{j \neq i} a_{ji} \right)
$$
The value $\sum_{j \neq i} a_{ji}$ is mined into the existing blockchain, appending at the end of the longest chain that contains the matrix of encrypted tinyVotes. 
4. When all voters have mined the sums of values that they have been sent, these are summed, giving the poll result
$$
\sum_i \sum_{j \neq i} a_{ji}.
$$


#### Peer-to-peer network
Online users constantly and regularly (every second) broadcast and receive the blockchain, as well as the tinyVotes. Depending on the total size of the network, the peers that one communicates with is either everyone, or the users that were online recently.


#### GUI
We have built a most beautiful GUI which visualises the live status of the p2p network, through which new users can connect, and some statistics of vote results once polls close. We are also working on visualising the blockchain in this.


#### Smartphone application
It would also be relatively easy to have the GUI run on a smartphone app (since we use Qt, which is portable), enabling people to connect, interact and vote straight from their phones.




# More detail:

The idea is to create an e-voting system that offers:

1. Full decentralisation: the users are collectively in charge of the process, there is no central authority;
2. Complete anonymity: the only agent aware of a user's vote is the user herself;
3. Verification: the voters can collectively prove that there is no vote manipulation,
i.e. for any type of fraud there will be a voter able to detect it.

Unfortunately, this is not possible, but we get close - some conditions are slightly relaxed. It is nevertheless a good idea to remember the initial goal and try to get ever closer.

----
## Technology
Easy: blockchain + homomorphic encryption in Python.

----
## Implementation

Suppose all votes are binary (0 or 1) throughout!
A non-binary voting system can easily be obtained from a binary one.

----
## Homomorphic encryption
A Homomorphic encryption is a function h such that

* h(x) is easy to compute from x;
* given h(x), it is not feasible to find any y (including x) such that h(y) = h(x);
* h(x+y) = h(x) ^ h(y) for some computable operation "^".

----
## Data

Every user is associated with the following data:

1. UserID, probably a string or a number;
2. Vote: 0 or 1;
3. Private key: some number;
4. Public key: which is h(vote + private key \* N), where N is an *initially agreed* number, larger than the total number of users.

Every user stores and remembers their corresponding quadruple; while the set of all pairs (UserID, Public Key) is available to all users via blockchain.

----
## Aggregation
An *aggregation* is used to describe and verify how a set of users voted. An aggregation is a triple of the form (sU, sV, sK), where

* sU is some set of users;
* sV is the sum of the votes of the users in sU;
* sK is the sum of the private keys of the users in sU.

An aggregation can be verified to be consistent - check if
h(sV + sK * N) equals the public keys corresponding to sU, combined with the "^" operation.


In general, it is unfeasible to create an aggregation in a malicious way under the assumptions for homomorphic encryption. Aggregation can be computed

* from a the private keys of a group of users, however every user only has their own private key;

* by combining smaller aggregations into a larger one.

Finally, an aggregation with the set of all users fully describes and verifies the outcome of an election - sV gives the total number of votes, and the figure must be genuine, since from h(x) it is not possible to find y such that h(x) = h(y).

----
## Computing Aggregations
Any user may declare their pair (userID, public_key) at any time, and store it in the blockchain for good.  However, an aggregation has to be computed to find the final result and this is trickiest part.  Here we need to relax the initial conditions a bit.

1.  We may relax the decentralisation condition - there could be third party agents, say aggregators, counting the votes.  For instance, Aggregator 1 computes an aggregation of the first 100 users, Aggregator 2 - the second 100 users, and so on.  Another Aggregator combines these aggregations into the final one.  In general, every tree with leaves corresponding to voters is a valid model for computing aggregations.  Directed acyclic graphs are also possible, but it seems pointless.  In a real election every bulletin is manually inspected by a governmental employee, so this assumption should not seem unrealistic.

2.  Another solution is to relax anonymity - it suffices for each voter to share their vote with one more voter.  Voter may split into pairs, compute pair aggregations, then quadruple aggregations and so one.  The partition could be random or trust-based.  Random pairing has the advantage of increasing the chance of pairing with a person with a different vote (an aggregation where all votes are the same exposes the votes of all included voters!).  Preference pairing has the advantage of not rising exposing your vote.

3.  Any combination of the two, combined with any tree structure is possible.  In general, there is a lot of room for creativity - onion routing to improve approach 2. is an idea to start with.  Of great help is the fact that any malicious vote manipulation will be immediately detected, and the responsible agent indentified, due to the ease and effectiveness of detecting weather or not an aggregation is consistent.


----
## Secure Aggregation
For a voter x let private_key(x) * N + vote(x) be called private_vote(x).
Let G (from Group) be a set of M users.
Under this protocol user x partitions their private_vote(x) into M integers that sum up to private_vote(x),
namely M integers a_1, ..., a_M such that Sum_i a_i = private_vote(x).
The second step is each voter to send each other voter in G one number a_j, and keep one for herself.
Next, every voter in G sums all received integers,
and declares the sum.
Finally, all declared sums are summed together,
and this number should equal the sum all private_votes over G.
An aggregation can easily be created from this sum.
Note that as long as at least two voters within the group are honest,
votes will remain anonymous.
This in a sense the best possible,
since it is impossible to guarantee anonymity if all but one voters are
malicious - the malicious voters may all vote 0 and retrieve the remaining vote as the result of the election.

----
## Blockchain

Blockchain technology is an umbrella term for technologies for decentralised data storage, distribution, verification and consensus building. A blockchain is a certain data structure, consisting of blocks, each of which have some contents and a header containing, among others, information about the block, a reference to the previous block, and a hash of the data contained in that block. (Ethereum extends this to decentralised computation, using 'smart contracts'.) Blockchains are useful when multiple parties need to read the same information, but any individual party's control of that data is undesired.

A blockchain ecosystem is network of replicated databases, either permissionless (i.e.~ peer-to-peer) or permissioned. It consists of one long chain of data blocks, each referring to the (hash of the) previous one, and uses digital signatures to prove identity and authenticity, and enforce read/write rights. Crucially, such a distributed ledger has mechanisms for making it hard to change historical records. Blocks are typically created at regular time intervals and/or with a certain (maximal) size, through 'mining' (hash computation).

The following are the main components of a blockchain system  - we exemplify each by explaining how Bitcoin has chosen to approach them:

* Consensus mechanism: longest chain rule - alternative blocks are disregarded (not needed in trusted networks). In Ethereum, such 'uncle nodes' are kept and receive currency for being referred to.

* Upgrade mechanism: vote by hashing power, freedom to adopt

* Participation criteria: pseudonymous, open (anyone can write/read/validate data and add blocks)

* Defence mechanism: computationally expensive mining, proof-of-work, i.e.~compute a hash with certain properties - data meddling requires reconstruction of all hashes since hacked block (alternative: proof-of-stake)

* Incentivisation mechanism: mining reward & transaction fees, (no incentive for storage/validation).


For more information, see for instance https://bitsonblocks.net/

APIs:
Apparently most used: https://github.com/blockchain/api-v1-client-python
ETH client: https://github.com/ethereum/pyethapp
Excellent basic intro: https://github.com/emunsing/tutorials/blob/master/BuildYourOwnBlockchain.ipynb



----
## Next steps

* Think of user interface.

* Find good libraries for blockchain and homomorphic encryption and build an early prototype.
