#coding:utf-8
import math
import random

pref = ""
inter_list = []
item_list = []

fo = [open("../data/random_split_train",'w'), open("../data/random_split_validation",'w'),open("../data/random_split_test",'w'),
     open("../data/time_split_train",'w'), open("../data/time_split_validation",'w'),open("../data/time_split_test",'w')]

for line in open("../data/Electronics_5core"):
    user_id, item_id, rating, time_stamp = line[:-1].split("\t")
    if user_id != pref:
        inter_num = len(inter_list)
        if inter_num < 5:
            inter_list = []
            item_list = []
        else:
            if inter_num < 10:
                val_test_num = 1
            else:
                val_test_num = int(round(inter_num * 0.1))
            train_num = int(inter_num - 2 * val_test_num)

            #---random_split---#
            rdm_list = list(inter_list)
            val_test_list = list(random.sample(rdm_list, 2 * val_test_num))
            rdm_list = list(set(rdm_list).difference(set(val_test_list)))
            val_list = list(random.sample(val_test_list, val_test_num))
            test_list = list(set(val_test_list).difference(set(val_list)))
            for i,r in rdm_list:
                fo[0].write(pref+'\t'+i+'\t'+r+"\n")
            for idx in range(val_test_num):
                fo[1].write(pref+"\t"+val_list[idx][0] + '\t' + val_list[idx][1] + '\n')
                fo[2].write(pref+"\t"+test_list[idx][0] + '\t' + test_list[idx][1] + '\n')
            #---random_split---#

            #---time_split---#
            val_test_list = list(inter_list)[-2*val_test_num:]
            train_list = list(inter_list)[:train_num]
            for i,r in train_list:
                fo[3].write(pref+"\t"+i+'\t'+r+"\n")
            for idx in range(2*val_test_num):
                if idx < val_test_num:
                    fo[4].write(pref+"\t"+val_test_list[idx][0]+'\t' + val_test_list[idx][1] + '\n')
                else:
                    fo[5].write(pref+"\t"+val_test_list[idx][0]+'\t' + val_test_list[idx][1] + '\n')
            #---time_split---#

            inter_list = []
            item_list = []

    if item_id not in item_list:
        inter_list.append((item_id,rating))
        item_list.append(item_id)
    pref = user_id

inter_num = len(inter_list)
if inter_num >= 5:
    if inter_num < 10:
        val_test_num = 1
    else:
        val_test_num = int(round(inter_num * 0.1))
    train_num = int(inter_num - 2 * val_test_num)
    #---random_split---#
    rdm_list = list(inter_list)
    val_test_list = list(random.sample(rdm_list, 2 * val_test_num))
    rdm_list = list(set(rdm_list).difference(set(val_test_list)))
    val_list = list(random.sample(val_test_list, val_test_num))
    test_list = list(set(val_test_list).difference(set(val_list)))
    for i,r in rdm_list:
        fo[0].write(pref+"\t"+i+'\t'+r+"\n")
    for idx in range(val_test_num):
        fo[1].write(pref+"\t"+val_list[idx][0] + '\t' + val_list[idx][1] + '\n')
        fo[2].write(pref+"\t"+test_list[idx][0] + '\t' + test_list[idx][1] + '\n')
    #---random_split---#

    #---time_split---#
    val_test_list = list(inter_list)[-2*val_test_num:]
    train_list = list(inter_list)[:train_num]
    for i,r in train_list:
        fo[3].write(pref+"\t"+i+'\t'+r+"\n")
    for idx in range(2*val_test_num):
        if idx < val_test_num:
            fo[4].write(pref+"\t"+val_test_list[idx][0]+'\t' + val_test_list[idx][1] + '\n')
        else:
            fo[5].write(pref+"\t"+val_test_list[idx][0]+'\t' + val_test_list[idx][1] + '\n')

    #---time_split---#

for fi in fo:
    fi.close()
