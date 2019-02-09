import os
import sys
import string


def run():
    try:
        if(len(sys.argv) < 2):
            raise ValueError
        source = sys.argv[1]
        target = sys.argv[2]
        length = None
        if not (source.isalpha() or target.isalpha()):
            raise Exception("Must be an alphabetic string")
        elif not(len(source) == len(target)):
            raise Exception("Need two words of the same length")
        if(len(sys.argv) > 3):
            length = int(sys.argv[3])
        dictionary = filterDict(len(source))
        dictionary.add(target)
        wordChain(source, target, dictionary, length)

    except Exception as e:
        print("{} {} {} not possible".format(source, target, length))
        print(e)
        exit()


def filterDict(l):
    dictionary = set()
    f = sys.stdin
    for line in f:
        word = line.strip("\n")
        if(len(word) == l):
            dictionary.add(word)
    return dictionary


def wordChain(source, target, dictionary, length):
    lengths = {}
    nextWords = {}
    path = []
    if(length == None):
        shortestPath(source, target, dictionary, lengths, nextWords, path)
    else:
        chain = [source]
        targetPath(source, target, dictionary, chain, length, path)
    if(path):
        print(' '.join(path))
    else:
        if not (length == None):
            print("{} {} {} not possible".format(source, target, length))
        else:
            print("{} {} not possible".format(source, target))


def diffOne(currWord, dictionary):
    diffOne = set()
    word = list(currWord)
    for x in range(len(currWord)):
        tempChar = word[x]
        for char in list(string.ascii_lowercase):
            word[x] = char
            tempWord = "".join(word)
            if(tempWord in dictionary and tempWord != currWord):
                diffOne.add(tempWord)
        word[x] = tempChar
    return diffOne


def shortestPath(source, target, dictionary, lengths, nextWords, solution):
    queue = []
    queue.append(source)
    lengths[source] = 0
    for word in dictionary:
        nextWords[word] = []
    nextWords[source] = []
    while (queue):
        solved = False
        for x in range(len(queue)):
            currWord = queue.pop(0)
            diff = diffOne(currWord, dictionary)
            for d in diff:
                nextWords[currWord].append(d)
                if not(d in lengths):
                    lengths[d] = lengths[currWord]+1
                    if(d == target):
                        solved = True
                    else:
                        queue.append(d)
        if(solved):
            break
    findShortestPath(source, target, nextWords, lengths, [], solution)


def targetPath(current, target, dictionary, chain, length, solution):
    currChain = chain.copy()
    currLevel = len(currChain)
    nextWords = diffOne(current, dictionary)
    if(currLevel == length - 1):
        if(target in nextWords):
            currChain.append(target)
            for word in currChain:
                solution.append(word)
            return
        else:
            return
    for word in nextWords:
        if(currLevel < length and word != target):
            if not(word in currChain):
                if(currLevel == len(currChain)):
                    currChain.append(word)
                else:
                    currChain[currLevel] = word
                targetPath(word, target, dictionary,
                           currChain, length, solution)
            if(solution):
                break


def findShortestPath(current, target, nextWords, lengths, path, solution):
    path.append(current)
    if(current == target):
        for w in path:
            solution.append(w)
        return
    else:
        for word in nextWords[current]:
            if(lengths[word] == lengths[current] + 1):
                findShortestPath(word, target, nextWords,
                                 lengths, path, solution)
            if(solution):
                break
    if(solution):
        return
    del path[-1]


def findTargetPath(current, target, nextWords, lengths, length, path):
    path.append(current)
    if(current == target):
        return
    else:
        for word in nextWords[current]:
            if(lengths[word] == lengths[current] + 1):
                return findTargetPath(word, target, nextWords, lengths, length, path)


if __name__ == "__main__":
    run()
