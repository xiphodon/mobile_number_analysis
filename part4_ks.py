#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/31 10:44
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : part4_ks.py
# @Software: PyCharm

import numpy as np
import time

def Calresult(predLabel, testLabel):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(len(predLabel)):
        if testLabel[i] == 0:
            if predLabel[i] == 0:
                TN += 1
            else:
                FP += 1
        else:
            if predLabel[i] == 1:
                TP += 1
            else:
                FN += 1

    if (TP + FN) == 0:
        TPR = 0
    else:
        TPR = TP / float(TP + FN)

    if (FP + TN) == 0:
        FPR = 0
    else:
        FPR = FP / float(FP + TN)

    return (TPR, FPR)


def Calresult2(predLabel, testLabel):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(len(predLabel)):
        if testLabel[i] == 0:
            if predLabel[i] == 0:
                TN += 1
            else:
                FP += 1
        else:
            if predLabel[i] == 1:
                TP += 1
            else:
                FN += 1

    if (TP + FN) == 0:
        TPR = 0
    else:
        TPR = TP / float(TP + FN)

    if (FP + TN) == 0:
        FPR = 0
    else:
        FPR = FP / float(FP + TN)

    return (TPR, FPR)



def ks_main(possibility, testLabel):
    length = len(possibility)
    # Sorting the predict result label and orgional label according to predicted possibility
    sort_dict = {}

    for i in range(length):
        sort_dict[i] = (possibility[i], testLabel[i])

    sorted_dict = sorted(sort_dict.items(), key=lambda item: item[1][0], reverse=True)

    sorted_possibility = [0] * length
    sorted_testLabel = [0] * length

    # Get re-ordered Perdict label and test label
    for i in range(length):
        sorted_possibility[i] = sorted_dict[i][1][0]
        sorted_testLabel[i] = sorted_dict[i][1][1]

    TPR_list = [0] * length
    FPR_list = [0] * length
    cal_list = [0] * length

    max_ks = 0
    cut_off = 0
    for i in range(length):

        cal_list[0:i + 1] = [1 for i in range(i + 1)]

        # TPR_list[i] = Calresult(cal_list, sorted_testLabel)[0]
        # FPR_list[i] = Calresult(cal_list, sorted_testLabel)[1]
        TPR_list[i], FPR_list[i] = Calresult(cal_list, sorted_testLabel)

        if (TPR_list[i] - FPR_list[i]) >= max_ks:
            max_ks = TPR_list[i] - FPR_list[i]
            cut_off = sorted_possibility[i]
            mx_index = i

    cut_off = np.log((1 - cut_off) / cut_off) * 50 / np.log(2) + 500
    return (TPR_list, FPR_list, max_ks, cut_off, mx_index)


def ks_main2(predict, target):

    length = len(target)
    predict_desc_index = np.argsort(predict)

    sorted_predict = [0] * length
    sorted_target = [0] * length

    for i in range(length):
        sorted_predict[i] = predict[predict_desc_index[-i]]
        sorted_target[i] = target[predict_desc_index[-i]]


    all_bad_sum = sum(sorted_target)
    all_good_sum = length - all_bad_sum

    x_axis_good = [0.0] * length
    x_axis_bad = [0.0] * length

    for i in range(1,length + 1):
        this_bad_sum = sum(sorted_target[:i])
        this_good_sum = len(sorted_target[:i]) - this_bad_sum

        x_axis_bad[i-1] = this_bad_sum / all_bad_sum
        x_axis_good[i-1] = this_good_sum / all_good_sum

    print(x_axis_good)
    print(x_axis_bad)

    x_axis_delta = np.array(x_axis_good) - np.array(x_axis_bad)
    print(x_axis_delta)
    return max(x_axis_delta)


    # TPR_list = [0] * length
    # FPR_list = [0] * length
    # cal_list = [0] * length
    #
    # max_ks = 0
    # cut_off = 0
    # for i in range(length):
    #
    #     cal_list[0:i + 1] = [1 for i in range(i + 1)]
    #
    #     TPR_list[i], FPR_list[i] = Calresult(cal_list, sorted_target)
    #
    #     if (TPR_list[i] - FPR_list[i]) >= max_ks:
    #         max_ks = TPR_list[i] - FPR_list[i]
    #         cut_off = sorted_predict[i]
    #         mx_index = i

    cut_off = np.log((1 - cut_off) / cut_off) * 50 / np.log(2) + 500
    return (TPR_list, FPR_list, max_ks, cut_off, mx_index)

def Score(defaultprobility):
    return list(map(lambda x:np.log((1 - x)/x) * 50 / np.log(2) + 500,defaultprobility))

def Score_2(defaultprobility):
    return list(map(lambda x:np.log2((1 - x)/x) * 50 + 500,defaultprobility))


if __name__ == "__main__":
    predict_list = [0.8, 0.6, 0.3, 0.1, 0.7, 0.4, 0.5, 0.8, 0.2, 0.4] *100
    target_list =  [  1,   0,   0,   0,   1,   1,   0,   1,   0,   0] *100

    time2 = time.time()
    max_ks2 = ks_main2(predict_list, target_list)
    print(max_ks2)
    score2 = Score_2(predict_list)
    # print(score2)
    d_time2 = time.time() - time2
    print(d_time2)


    time1 = time.time()
    TPR_list, FPR_list, max_ks, cut_off, mx_index = ks_main(predict_list, target_list)
    print(max_ks)
    score = Score(predict_list)
    # print(score)
    d_time1 = time.time() - time1
    print(d_time1)


