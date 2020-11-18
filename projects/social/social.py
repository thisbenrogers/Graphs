import random

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.friendship_count = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def get_friends(self, vertex_id):
        """
        Get all friends (edges) of a vertex.
        """
        return self.friendships[vertex_id]

    def bfs(self, starting_vertex, destination_vertex):
        visited = set()
        q = [[starting_vertex]]
        if starting_vertex == destination_vertex:
            return q[0]
        while q:
            path = q.pop(0)
            node = path[-1]
            if node not in visited:
                friends = self.get_friends(node)
                for friend in friends:
                    new_path = list(path)
                    new_path.append(friend)
                    q.append(new_path)
                    if friend == destination_vertex:
                        return new_path
                visited.add(node)
        return None

    def fisher_yates_shuffle(self, l):
        for i in range(0, len(l)):
            random_index = random.randint(i, len(l) - 1)
            l[random_index], l[i] = l[i], l[random_index]

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # Create friendships
        friendship_combos = []
        total_friendships = avg_friendships * num_users

        # TODO find a way to miss this nested for loop. 
        # TODO "You can avoid this by only creating friendships where user1 < user2"
        for user_id in range(1, num_users + 1):
            for friend_id in range(user_id + 1, num_users + 1):
                friendship_combos.append((user_id, friend_id))

        self.fisher_yates_shuffle(friendship_combos)

        friendships_to_make = friendship_combos[:(total_friendships // 2)]
        for friendship in friendships_to_make:
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        paths = {}  # Note that this is a dictionary, not a set

        paths[user_id] = []
        
        # initialize a 'friends' list
        friends = list(self.get_friends(user_id))

        # put all the connected users in self.users
        while len(friends) > 0:
            new_friends = []
            for friend in friends:
                curr_friend = friends.pop(0)
                if curr_friend not in paths.keys():
                    paths[curr_friend] = []
                    new_friends = self.get_friends(curr_friend)
            friends.extend(new_friends)

        # iterate over paths, and add the return from bfs as the value
        for user in paths.keys():
            paths[user] = self.bfs(user_id, user)

        return paths


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
