import git

class Event:
    """
    Represents an event that we can push to the server.  Gets created
    and returned by the build_* functions, and sent to the actual server
    by a Sender object.
    """
    
    def __init__(self, type, timestamp, user_email, data):
        self.type = type
        self.timestamp = timestamp
        self.user_email = user_email
        
        # a dict of event-type specific info (gets parsed by Sender)
        self.data = data

class EventBuilder:
    """
    Builds and returns correctly formatted events.
    """
    
    def __init__(self, repo_dir, user_email):
        self.repo = git.Repo(repo_dir)
        self.user_email = user_email
    
    def build_push(self):
        raise NotImplementedException("Must implement push!")

    def build_commit(self):
        # get the commit we're going to operate on
        commit = self.repo.head.commit # latest commit for this repository
        
        # all the data we'll need for this commit:
        #  active_branch: the current branch
        #  author_email: the email of the author of the commit
        #  hash: the sha hash (in hex) of the commit
        #  message: the commit message
        #  deletions: number of lines deleted
        #  insertions: number of lines inserted
        #  files: number of files modified
        data = {
            "active_branch": self.repo.active_branch.name,
            "commit_hash": commit.hexsha,
            "author_email": commit.author.email,
            "message": commit.message,
            "deletions": commit.stats.total["deletions"],
            "insertions": commit.stats.total["insertions"],
            "files": commit.stats.total["files"],
            }
        
        return Event("commit", commit.committed_date,
                     self.user_email, data)

    def build_branch(self):
        raise NotImplementedException("Must implement branch!")

    def build_checkout(self):
        raise NotImplementedException("Must implement checkout!")
