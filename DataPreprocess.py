import os
import pandas as pd

def save_data(dir, texts, tags, start, end):
    data_file = dir
    num = 0
    space = 0
    lb = 0
    split_chars = ['。' , '！' , '？' , '，', '.' , ',' , ';' , ':', '!', '；' , '．' , '？', '；', '。']
    if os.path.exists(data_file):
        os.remove(data_file)
    with open(data_file, 'a', encoding = 'utf-8') as f:
        for k in range(start, end):
            text_ = texts[k]
            tag_ = tags[k]
            for p in range(len(text_)):
                if text_[p] == '\n':
                    #                     f.write('LB'+'\t'+tag_[p]+'\n')
                    space += 1
                elif text_[p] == ' ':
                    #                     f.write('SPACE'+'\t'+tag_[p]+'\n')
                    lb += 1
                elif text_[p] in split_chars:
                    num += 1
                    if text_[p] == '.' or text_[p] == '．':
                        # if p != 0 and p < len(text_):
                            if not text_[p - 1].isalpha() or not text_[p + 1].isalpha():
                                f.write(text_[p] + '\t' + tag_[p] + '\n')
                                continue
                    f.write(text_[p] + '\t' + tag_[p] + '\n\n')
                else:
                    f.write(text_[p] + '\t' + tag_[p] + '\n')
    print(space, lb)
    return num


def get_train_data(data_dir, cv_ratio=0.2, get_test=True):
    texts = []
    tags = []

    fileidxs = set()
    for filename in os.listdir(data_dir):
        fileidxs.add(filename.split('.')[0])

    for fileidx in fileidxs:

        with open(data_dir + fileidx + '.txt', 'rb') as f:
            text = f.read().decode('utf-8')
        text_list = [char for char in text]

        tag = pd.read_csv(data_dir + fileidx + '.ann', header=None, sep='\t')
        tag_list = ['O' for _ in range(len(text_list))]

        for i in range(tag.shape[0]):
            tag_item = tag.iloc[i][1].split(' ')
            cls, start, end = tag_item[0], int(tag_item[1]), int(tag_item[-1])

            tag_list[start] = 'B-' + cls
            for j in range(start + 1, end):
                tag_list[j] = 'I-' + cls
        assert (len(text_list) == len(tag_list))
        texts.append(text_list)
        tags.append(tag_list)

    split_chars = ['。', '！', '？', '，']
    train_num = 0
    dev_num = 0
    test_num = 0
    doc_dev_num = int(len(texts) * cv_ratio)

    train_num = save_data('data1109/ruijin_train.data', texts, tags, 0, len(texts) - doc_dev_num)
    if get_test:
        dev_num = save_data('data/ruijin_dev.data', texts, tags, len(texts) - doc_dev_num,
                            len(texts) - doc_dev_num // 2)
        test_num = save_data('data/ruijin_test.data', texts, tags, len(texts) - doc_dev_num // 2, len(texts))
    else:
        dev_num = save_data('data1109/ruijin_dev.data', texts, tags, len(texts) - doc_dev_num, len(texts))

    print('train_num:{}, dev_num:{}, test_num:{}'.format(train_num, dev_num, test_num))

def get_test_data(data_dir):
    split_chars = ['。', '！', '？', '，', '.', ',', '、', ';', ':', '!', '；', '．', '？', '；']
    texts = []
    num = 0
    space = 0
    lb = 0
    ROOT_DIR = 'data1109/test/'
    for filename in os.listdir(data_dir):
        with open('raw_data/test/' + filename, 'rb') as f:
            text = f.read().decode('utf-8')
        text_ = [char for char in text]
        w_path = os.path.join(ROOT_DIR, filename)
        with open(w_path, 'a', encoding='utf-8') as f:
            for p in range(len(text_)):
                if text_[p] == '\n':
                    space += 1
                elif text_[p] == ' ':
                    lb += 1
                elif text_[p] in split_chars:
                    num += 1
                    if text_[p] == '.' or text_[p] == '．':
                        # if p != 0 and p < len(text_):
                            if not text_[p - 1].isalpha() or not text_[p + 1].isalpha():
                                f.write(text_[p]  + '\n')
                                continue
                    f.write(text_[p] + '\n\n')
                else:
                    f.write(text_[p]  + '\n')







get_train_data(data_dir='raw_data/train/',cv_ratio=0.1)
# get_test_data('raw_data/test/')


