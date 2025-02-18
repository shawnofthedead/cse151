import numpy as np
import sys, csv, math
from sklearn.metrics import confusion_matrix
if __name__ == '__main__':
    data = np.genfromtxt('SpamDataPruned.csv', delimiter=",")
    np.random.seed(0)
    np.random.shuffle(data)
    train_num = int(data.shape[0] * 0.9)
    X_train = data[:train_num, :-1]
    Y_train = data[:train_num, -1]
    X_test = data[train_num:, :-1]
    Y_test = data[train_num:, -1]

    spam = [i for i in Y_train if i == 1]
    spam = len(spam)
    ham = len(Y_train) - spam
    Pspam = float(spam)/len(Y_train)
    Pham = float(ham)/len(Y_train)

    WordGivenSpamList = []
    WordGivenHamList = []

    for i in X_train.T:
        X_data = zip(i, Y_train)
        cntWordGivenSpam = 0
        cntWordGivenHam = 0
        for x, y in X_data:
            if y == 1:
                cntWordGivenSpam += x
            else:
                cntWordGivenHam += x

        WordGivenSpamList.append(cntWordGivenSpam)
        WordGivenHamList.append(cntWordGivenHam)
    sumWGSL = sum(WordGivenSpamList)
    sumWGHL = sum(WordGivenHamList)


    numofTerms = len(WordGivenHamList)


    PwordGivenSpamLst = [float(i+1)/(sumWGSL + numofTerms) for i in WordGivenSpamList]
    PwordGivenHamLst = [float(i+1)/(sumWGHL + numofTerms) for i in WordGivenHamList]

    pred_list = []
    for i in X_test:
        pred_spam = math.log(Pspam)
        pred_ham = math.log(Pham)
        for ind, x in list(enumerate(i)):
            if x != 0:
                pred_spam += math.log(PwordGivenSpamLst[ind])
                pred_ham += math.log(PwordGivenHamLst[ind])

        pred = max(pred_spam, pred_ham)
        if pred == pred_spam:
            pred_list.append(1)
        else:
            pred_list.append(0)

    acc = [1 if x == y else 0 for x, y in zip(pred_list, Y_test)]

    # print out the accuracy
    print(sum(acc)/len(Y_test))

    con = confusion_matrix(Y_test,pred_list)
    np.savetxt("matrix.csv",con,delimiter=',')
