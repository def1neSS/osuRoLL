import random

class M_FunRoLL(object):
    
    pts = {
        '+' : 12,
        '-' : 4
    }

    def roll():

        file_chall = open("data\M_FunRoLL\Challenges.txt", "r")
        list = []

        while True:
            list.append(file_chall.readline())
            if not line:
                break

        file_chall.close

        return random.choice(list)


