import random
from surprise import Dataset
from surprise import Reader
from surprise import SVDpp

from src.build_metric import Metrics5 as Metrics


#按行读取文件
def yield_line(file_path):
    with open(file_path) as f:
        line = f.readline()
        while line:
            yield line.strip()
            line = f.readline()

# 获取所有的items和权重
def get_items(file_path):
    itemsmap = {}
    for line in yield_line(file_path):
        u, i, r = line.split("\t", 2)
        itemsmap.setdefault(i, 0)
        itemsmap[i] += 1
    return zip(*(itemsmap.items()))


def test(model, sample_ratio=50, sample_weight=None, all=False, at_k = 50):
    print("\t\ttest model start...")
    metrics = Metrics(min(sample_ratio, at_k))
    u_is_map = {}
    for line in yield_line(test_file_path):
        u, i, r = line.split("\t", 2)
        u_is_map.setdefault(u, set([]))
        u_is_map[u].add(i)

    for u, i_s in u_is_map.items():
        probs, targets = [], []
        for i in i_s:
            probs.append(model.predict(u ,i).est)
            targets.append(1)

        if all:
            sample_item = items
        else:
            sample_item = random.choices(items, cum_weights=sample_weight, k=sample_ratio*len(i_s))
        #test_items = sample_item
        #print(sample_item)
        for item in sample_item:
            if item in i_s:
                continue
            else:
                #probs.append(model.estimate(u, item))
                probs.append(model.predict(u ,item).est)
                targets.append(0)
        metrics.append(probs, targets)
    print("\t\ttest model end!")
    metrics.build()
    print("\t\t" + str(metrics))

if __name__ == '__main__':

    time_splits = [True, False]
    pop_samples = [False, True]
    sample_ratios = [10, 50]
    base_path = "E://workspace//pycharm-workspace//recsys//data"

    reader = Reader(line_format='user item rating', sep='\t')

    #是否随机
    for time_split in time_splits:
        print("time split: %s." % str(time_split))
        if time_split:
            train_file_path = base_path + "//time_split_train"
            test_file_path = base_path + "//time_split_test"
        else:
            train_file_path = base_path + "//random_split_train"
            test_file_path = base_path + "//random_split_test"
        train_data = Dataset.load_from_file(train_file_path, reader=reader).build_full_trainset()

        items, weight = get_items(train_file_path)

        # 权重前缀和，加快采样速度
        cum_weight, cum = [], 0.
        for w in weight:
            cum_weight.append(cum + w)
            cum += w

        # 初始化模型
        model = SVDpp(n_epochs=100, verbose=True)

        # 训练模型
        print("\ttrain model start...")
        model.fit(train_data)
        print("\ttrain model end!")


        # 采样测试
        for sample_ratio in sample_ratios:
            for pop_sample in [cum_weight, None]:
                print("\tsample ratio: %d, popularity sample: %s." % (sample_ratio, str(pop_sample is not None)))
                test(model, sample_ratio, pop_sample)

        # 全排序测试
        print("\tsample ratio: %s, popularity sample: %s." % (str(None), str(None)))
        test(model, all=True)

