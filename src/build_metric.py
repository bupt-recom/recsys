from src.evaluate import Metric

class Metrics:
    def __init__(self, k):
        self.call = Metric()
        self.precision, self.recall, self.auc, self.ndcg, self.acc, self.map, self.mrr = 0., 0., 0., 0., 0., 0., 0.
        self.hr_k, self.hr_total, self.hr = 0., 0., 0.
        self.f1 = 0.
        self.k = k
        self.count = 0

    def append(self, probs, targets):
        self.precision += self.call.precision(probs, targets, self.k)
        self.recall += self.call.recall(probs, targets, self.k)
        self.auc += self.call.auc(probs, targets)
        self.ndcg += self.call.ndcg(probs, targets, self.k)
        self.acc += self.call.accuracy(probs, targets)
        self.map += self.call.mAp(probs, targets)
        self.mrr += self.call.mrr(probs, targets)
        hr_k, hr_total = self.call.hr(probs, targets, self.k)
        self.hr_k += hr_k
        self.hr_total += hr_total
        self.count += 1

    def build(self):
        self.precision /= self.count
        self.recall /= self.count
        self.auc /= self.count
        self.ndcg /= self.count
        self.acc /= self.count
        self.map /= self.count
        self.mrr /= self.count
        self.hr = self.hr_k / self.hr_total
        self.f1 = 2 * self.precision * self.recall / (self.precision + self.recall)

    def __str__(self):
        return "precision: %.6f, recall: %.6f, auc: %.6f, ndcg: %.6f, acc: %.6f, map: %.6f, mrr: %.6f, hr: %.6f, f1: %.6f" \
               % (self.precision, self.recall, self.auc, self.ndcg, self.acc, self.map, self.mrr, self.hr, self.f1)


#
class Metrics5:
    def __init__(self, k):
        self.call = Metric()
        self.precision, self.recall = 0., 0.
        self.k = 5
        self.count = 0

    def append(self, probs, targets):
        self.precision += self.call.precision(probs, targets, self.k)
        self.recall += self.call.recall(probs, targets, self.k)
        self.count += 1

    def build(self):
        self.precision /= self.count
        self.recall /= self.count

    def __str__(self):
        return "precision: %.6f, recall: %.6f" \
               % (self.precision, self.recall)