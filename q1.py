from math import log

# encodes vector of 0's and 1's => indicatoing the words presence in the sentence
def Encode(sent, wordls):
    returnls = []
    words = sent.split()[1:]
    encountered = []
    for word in wordls:
        if word in encountered:
            continue
        if word in words:
            returnls += [1]
        else:
            returnls += [0]
        encountered += [word]

    return returnls


# generate a list of 2D vectors which correspond to the good/bad inferences of the statement
def Inference(TestSent, wordls, good_dict, bad_dict):
    wordls = list(wordls)
    inferences = []

    for sent in TestSent:
        encoding = Encode(sent, wordls)
        prob_good = 0
        prob_bad = 0
        # use logs to counteract underflow
        for i in range(len(encoding)):
            if encoding[i] == 1:
                # contains word
                prob_good += log(good_dict[wordls[i]], 10)
                prob_bad += log(bad_dict[wordls[i]], 10)
            else:
                # dos not contain word
                prob_good += log(1 - good_dict[wordls[i]], 10)
                prob_bad += log(1 - bad_dict[wordls[i]], 10)
        # add calculated probs to list
        inferences += [[prob_good, prob_bad]]
    return inferences


def Calc_prob(inferences, good_prob, bad_prob):
    num = inferences[0] * good_prob
    den = (inferences[0] * good_prob) + (inferences[1] + bad_prob)
    ans = num / den
    ans *= 100
    return round(ans, 2)


# MAIN
if __name__ == "__main__":
    # capture input
    raw_training_data = []  # array of arrays containing raw words per review
    for i in range(12):
        tmp = input().split()
        raw_training_data += [tmp]

    # get Y-class probabilities {P(good) , P(bad)}
    good = 0
    bad = 0
    for i in raw_training_data:
        tmp = int(i[0])
        if tmp == 1:
            good += 1
        else:
            bad += 1

    p_good = good / len(raw_training_data)
    p_bad = bad / len(raw_training_data)

    # draw ClassConditionalModel => 3 steps
    # 1.) count words and create a word_set
    word_set = set()
    for sentence in raw_training_data:
        for i in range(1, len(sentence)):
            # if len(sentence[i]) > 2:
            word_set.add(sentence[i])

    # create both dicts
    good_dict = dict()
    bad_dict = dict()
    for word in word_set:
        good_dict[word] = 0
        bad_dict[word] = 0

    # 2.) count good occurances / word_set
    for sentence in raw_training_data:
        if int(sentence[0]) == 1:
            for i in range(1, len(sentence)):
                # if len(sentence[i]) > 2:
                good_dict[sentence[i]] += 1 / good

    # 3.) count bad occurances / word_set
    for sentence in raw_training_data:
        if int(sentence[0]) == -1:
            for i in range(1, len(sentence)):
                # if len(sentence[i]) > 2:
                bad_dict[sentence[i]] += 1 / bad

    # smoothing
    k = 1
    # first loop through good_dict
    for x, pg in good_dict.items():
        if pg == 0:
            good_dict[x] = ((pg * good) + k) / (good + (len(word_set) * k))
            pb = bad_dict[x]
            bad_dict[x] = ((pb * bad) + k) / (bad + (len(word_set) * k))
    # secondly loop the bad_dict
    for x, pb in bad_dict.items():
        if pb == 0:
            bad_dict[x] = ((pb * bad) + k) / (bad + (len(word_set) * k))
            pg = good_dict[x]
            good_dict[x] = ((pg * good) + k) / (good + (len(word_set) * k))

    # print class contiional model
    for i in word_set:
        print(
            i + "\t" + str(round(good_dict[i], 4)) + "\t\t" + str(round(bad_dict[i], 4))
        )

    TestData = [
        "1 the service was great",
        "1 what a lovely restaurant",
        "1 the food the service and the restaurant was great",
        "-1 the service is terrible",
        "-1 the food tasted awful",
        "-1 this is a bad restaurant",
    ]

    print("\n")
    inferences = Inference(TestData, word_set, good_dict, bad_dict)
    print(inferences)
    print("\n")

    # finally print probabilities
    # Dont judge my english :(
    for i in range(len(TestData)):
        print(
            'The Statement: "'
            + TestData[i]
            + ' " is '
            + str(Calc_prob(inferences[i], p_good, p_bad))
            + "% chance a Good Review"
        )
