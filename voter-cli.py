import sys

help = '''usage: <command> [<args>]

<command> must be one of the following:
    sync
    vote
    status
    server

dav sync [hostname=localhost]     Fetches an election description from a URL.

dav vote election vote            Casts a vote in a specified election.

dav status [election=all]         Prints the status of a specified election, or
                                  all registered elections in case the first
                                  argument is not specified.

dav server                        Makes the host DAV server, allowing voters
                                  to sync to this host.
'''

def vote():
    raise NotImplementedError()


def status():
    raise NotImplementedError()


def sync_wrapper():
    import sync
    if len(sys.argv) < 2:
        hostname = "localhost"
    else:
        hostname = sys.argv[2]
    sync.sync(hostname)

def vote_wrapper():
    import vote
    if len(sys.argv) < 2:
        hostname = "10.21.209.229"
    else:
        hostname = sys.argv[2]
    vote.vote(hostname)
    
def server_wrapper():
    import server
    if len(sys.argv) < 5:
        server.serve(0, {})
    else:
        voter_id = int(sys.argv[2])
        friend_id = int(sys.argv[3])
        friend_ip = sys.argv[4]
        friend_port = int(sys.argv[5])
        server.serve(voter_id, {friend_id : (friend_ip, friend_port)})

def main():
    commands = {
        "sync" : sync_wrapper,
        "vote" : vote_wrapper,
        "status" : status,
        "server" : server_wrapper,
        }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(help)
        return

    commands[sys.argv[1]]()

if __name__ == "__main__":
    main()
