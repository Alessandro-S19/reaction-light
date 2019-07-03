from random import randint
import csv

wizard = {}
wizardcache = {}
cache = {}


def readcache():
    try:
        with open("cache.csv", "r") as f:
            r = csv.reader(f, delimiter=",")
            for row in r:
                cache[row[0]] = row[1]
    except FileNotFoundError:
        print("No cache.csv file found. It will be created on the next wizard run.")


def get(user, channel):
    global wizard
    for i in wizard:
        wizuser = wizard[i][0]
        wizchannel = wizard[i][1]
        r_id = wizard[i][2]
        step = wizard[i][3]
        if wizuser == user and wizchannel == channel:
            return step, r_id
    return None, None


def getch(r):
    return wizardcache[r][0][0]


def getcombo(r):
    with open(str(r) + ".csv", "r") as f:
        r = csv.reader(f, delimiter=",")
        return [i for i in r]


def addids(message_id, r):
    with open("cache.csv", "a") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow([message_id, r])


def getids(message_id):
    if message_id in cache:
        return cache[message_id]
    return None


def getreactions(r):
    with open(r + ".csv", "r") as f:
        r = csv.reader(f, delimiter=",")
        reactions = {}
        for row in r:
            try:
                reactions[row[0]] = int(row[1])
            except IndexError:
                pass
        return reactions


def listen(user, channel):
    global wizard
    r = str(randint(0, 100000))
    ids = {}

    try:
        with open("id.csv", "r") as f:
            read = csv.reader(f, delimiter=",")
            for i in read:
                ids[i[0]] = i[1:]
        while r in ids:
            r = str(randint(0, 100000))
    except FileNotFoundError:
        print("Creating id.csv")

    ids[r] = [str(user), str(channel)]
    with open("id.csv", "w") as f:
        w = csv.writer(f, delimiter=",")
        for i in ids:
            row = [i, ids[i][0], ids[i][1]]
            w.writerow(row)

    wizard[r] = [str(user), str(channel), r, 1]
    print("Created entry in Wizard: " + r)


def step1(r, role_channel):
    global wizard
    global wizardcache
    wizardcache[r] = [[role_channel]]
    wizard[r][3] += 1  # Set step2 (was 1)


def step2(r, role, emoji, done=False):
    global wizard
    global wizardcache
    if done:
        wizard[r][3] += 1  # Set step3 (was 2)
        with open(str(r) + ".csv", "a") as f:
            w = csv.writer(f, delimiter=",")
            for i in wizardcache[r]:
                w.writerow(i)
        print("Done adding combos and saved.")
        return
    combo = [emoji, role]
    print("Added " + emoji + " : " + role + " combo.")
    wizardcache[r].append(combo)


def end(r):
    del wizard[r]
    readcache()

readcache()