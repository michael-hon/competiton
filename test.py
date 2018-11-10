import codecs
import os
def load_data(path):
    sentences = [[]]
    index = [[]]
    with codecs.open(path, 'r', 'utf8') as reader:
        i = 0
        for line in reader:
            i += 1
            line = line.strip()
            if not line:
                if len(sentences[-1]) > 0:
                    sentences.append([])
                    index.append([])
                continue
            index[-1].append(i)
            sentences[-1].append(line)
    return sentences, index

def max_length(sentences, index):
    m_length = -1000000
    i = -1
    j = 0
    for sentence in sentences:
        length = len(sentence)
        j += 1
        if length > m_length:
            m_length = length
            i = j
    return m_length, index[i-1]



# sentences, index = load_data('data1109/ruijin_train.data')
# length, i = max_length(sentences, index)
# print(length)
# print(i)


ROOT_DIR = 'data1109/test/'
for filename in os.listdir(ROOT_DIR):
    filepath = os.path.join(ROOT_DIR, filename)
    sentences, index = load_data(filepath)
    length, i = max_length(sentences, index)
    print(filename, ':')
    print(length)
    print(i)
    print()
    print()
