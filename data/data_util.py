
def yield_line(file_path):
    with open(file_path) as f:
        line = f.readline()
        while line:
            yield line.strip()
            line = f.readline()

umap, imap = {}, {}
train_line_cnt = 0

for line in yield_line("E://workspace//pycharm-workspace//recsys//data//random_split_train"):
    u, i, r = line.split("\t")
    umap.setdefault(u, len(umap) + 1)
    imap.setdefault(i, len(imap) + 1)
    train_line_cnt += 1

for line in yield_line("E://workspace//pycharm-workspace//recsys//data//random_split_test"):
    u, i, r = line.split("\t")
    umap.setdefault(u, len(umap) + 1)
    imap.setdefault(i, len(imap) + 1)

f = open("random_split_train.mm", "w")
print >> f, "%%MatrixMarket matrix coordinate real general"
print >> f, len(umap), len(imap), train_line_cnt
for line in yield_line("E://workspace//pycharm-workspace//recsys//data//random_split_train"):
    u, i, r = line.split("\t")
    print >> f, "%d\t%d\t%s" % (umap[u], imap[i], r)
f.close()

f = open("random_split_test.index", "w")
for line in yield_line("E://workspace//pycharm-workspace//recsys//data//random_split_test"):
    u, i, r = line.split("\t")
    print >> f, "%d\t%d\t%s" % (umap[u], imap[i], r)
f.close()