import random
import numpy as np 
from mrec import load_fast_sparse_matrix
from mrec.base_recommender import BaseRecommender
from mrec.item_similarity.slim import SLIM
from src.build_metric import Metrics as Metrics


def yield_line(file_path):
    with open(file_path) as f:
        f.readline()
        f.readline()
        line = f.readline()
        while line:
            yield line.strip()
            line = f.readline()

def get_items(file_path):
    itemsmap = {}
    for line in yield_line(file_path):
        u, i, r = line.split("\t", 2)
        u = int(u)-1
        i = int(i)-1
        itemsmap.setdefault(i, 0)
        itemsmap[i] += 1
    return zip(*(itemsmap.items()))


def test(model, dataset, sample_ratio=50, sample_weight=None, all=False, at_k = 50):
    print("\t\ttest model start...")
    metrics = Metrics(min(sample_ratio, at_k))
    u_is_map = {}
    for line in yield_line(test_file_path):
        u, i, r = line.split("\t", 2)
        u = int(u)-1
        i = int(i)-1
        u_is_map.setdefault(u, set([]))
        u_is_map[u].add(i)

    # recs = model.batch_recommend_items(dataset,max_items=60000, show_progress=True)
    # for uuu in range(100):
    #     for iii,score in recs[uuu]:
    #         print(uuu,iii,score)
    # res = (dataset[u, :] * model.similarity_matrix.T).toarray()[0]
    for u, i_s in u_is_map.items():
        res = (dataset[u, :] * model.similarity_matrix.T).toarray()[0]
        probs, targets = [], []
        for i in i_s:
            probs.append(res[i])
            targets.append(1)

        if all:
            sample_item = items
        else:
            sample_item = np.random.choice(items, size=sample_ratio*len(i_s), replace=False, p=sample_weight)
            #sample_item = np.random.choice(items, size=3, replace=False, p=sample_weight)
        #test_items = sample_item
        #print(sample_item)
        
        for item in sample_item:
            if item in i_s:
                continue
            else:
                #probs.append(model.estimate(u, item))
                probs.append(res[item])
                targets.append(0)
        tmp = zip(probs, targets)
        random.shuffle(tmp)
        probs, targets = zip(*tmp)
        metrics.append(probs, targets)
    print("\t\ttest model end!")
    metrics.build()
    print("\t\t" + str(metrics))

if __name__ == '__main__':
    
    time_splits = [True]
    pop_samples = [False, True]
    sample_ratios = [10, 50]
    base_path = "E://workspace//pycharm-workspace//recsys//data"


    for time_split in time_splits:
        print("time split: %s." % str(time_split))
        if time_split:
            train_file_path = base_path + "//time_split_train.mm"
            test_file_path = base_path + "//time_split_test.index"
            model = BaseRecommender.load("src/time_model.npz")
        else:
            train_file_path = base_path + "//random_split_train.mm"
            test_file_path = base_path + "//random_split_test.index"
            model = BaseRecommender.load("src/random_model.npz")

        train_data = load_fast_sparse_matrix('mm', open(train_file_path))

        items, weight = get_items(train_file_path)


        weight = np.array(weight) / (sum(weight) * 1.0)

        # model = SLIM()

        # print("\ttrain model start...")
        # model.fit(train_data)
        # print("\ttrain model end!")

        # if time_split:
        #     model.save("time_model.npz")
        # else:
        #     model.save("random_model.npz")

        for sample_ratio in sample_ratios:
            for pop_sample in [weight, None]:
                print("\tsample ratio: %d, popularity sample: %s." % (sample_ratio, str(pop_sample is not None)))
                test(model, train_data.X, sample_ratio, pop_sample)
        
        print "\tsample ratio: %s, popularity sample: %s." % (str(None), str(None))
        test(model, train_data.X, all=True)