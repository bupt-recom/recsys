#coding:utf-8
from sklearn.metrics import roc_auc_score, f1_score
import numpy as np
import math

class Metric(object):
    def auc(self, probs, targets):
    # probs represents the prediction probability ([0.0, 1.0])
    # targets represents the real category (0 or 1)
        return roc_auc_score(targets, probs)
    
    def ndcg(self, probs, targets, k = 10):
        def DCG(label_list):
            dcgsum = 0
            for i in range(len(label_list)):
                dcg = (2**label_list[i] - 1)/math.log(i+2, 2)
                dcgsum += dcg
            return dcgsum
        def NDCG(label_list):
            dcg = DCG(label_list[0:k])
            ideal_list = sorted(label_list, reverse=True)
            ideal_dcg = DCG(ideal_list[0:k])
            if ideal_dcg == 0:
                return 0
            return dcg/ideal_dcg

        prob_tag = zip(probs, targets) 
        tmp = sorted(prob_tag, key = lambda x:-x[0])
        label_list = []
        for p,t in tmp:
            label_list.append(t)
        return NDCG(label_list)
    
    def mAp(self, probs, targets):
        prob_tag = zip(probs, targets)
        ranklist = sorted(prob_tag, key=lambda x:x[0], reverse=True)
        pos = 0.
        AP = 0.
        for idx,(prob,tag) in enumerate(ranklist):
            if tag == 1.0:
                pos += 1.
                AP += pos/(idx+1)
        return AP / pos

    def hr(self, probs, targets, k = 10):
        total_pos = targets.count(1)
        prob_tag = zip(probs, targets)
        ranklist = sorted(prob_tag, key=lambda x:x[0], reverse=True)[:k]
        k_pos = 0
        for p,t in ranklist:
            if t == 1:
                k_pos +=1
        return k_pos, total_pos

    def precision(self, probs, targets, k = 10):
        prob_tag = zip(probs, targets)
        ranklist = sorted(prob_tag, key=lambda x: x[0], reverse=True)[:k]
        k_pos = 0
        for p, t in ranklist:
            if t == 1:
                k_pos += 1.
        return k_pos / k


    def recall(self, probs, targets, k = 10):
        total_pos = targets.count(1)
        prob_tag = zip(probs, targets)
        ranklist = sorted(prob_tag, key=lambda x: x[0], reverse=True)[:k]
        k_pos = 0
        for p, t in ranklist:
            if t == 1:
                k_pos += 1.
        return k_pos / total_pos

    def f1(self, probs, targets, threshold = 0.5):
        pre = (np.array(probs) >= threshold).astype(int)
        tar = np.array(targets)
        return f1_score(tar, pre)

    def accuracy(self, probs, targets, threshold = 0.5):
        pre = (np.array(probs) >= threshold).astype(int)
        tar = np.array(targets)
        return np.sum((pre == tar).astype(float)) / pre.size

    def mrr(self, probs, targets):
        prob_tag = zip(probs, targets)
        ranklist = sorted(prob_tag, key=lambda x: x[0], reverse=True)
        for idx,(prob, tag) in enumerate(ranklist):
            if tag == 1.0:
                return 1.0 / (idx + 1)
        return 0
