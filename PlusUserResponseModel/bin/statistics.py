# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt


def plot_distribution(file):
    f = open(file, 'r')
    is_reply_list = [0]*8
    not_reply_list = [0]*8
    print "dsdsd"
    for line in f:
        toks = line.split('\t')
        for tok in toks[1:]:
            item = tok.split(':')
            assert len(item) == 4
            response = int(item[1])
            scale = int(item[2])
            if response == 1:
                is_reply_list[scale-1] += 1
            else:
                not_reply_list[scale-1] += 1

    fig, ax = plt.subplots()
    index = np.arange(8)
    bar_width = 0.35

    opacity = 0.4
    is_reply = plt.bar(index, is_reply_list, bar_width, alpha=opacity, color='b', label='Reply')
    not_reply = plt.bar(index + bar_width, not_reply_list, bar_width, alpha=opacity, color='r', label='Not Reply')

    plt.xlabel('Scale')
    plt.ylabel('Numbers')
    plt.title('Reaction for different company stage')
    plt.xticks(index + bar_width, ('W', 'T', 'A', 'B', 'C', 'D', 'S', 'N'))
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    file = '../raw/chat_feature.txt'
    plot_distribution(file)