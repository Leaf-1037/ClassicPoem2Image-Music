import re                           # 正则表达式库
import jieba                        # 结巴分词
import jieba.posseg                 # 词性获取
import collections                  # 词频统计库
from TxtJson import Transform_Form
from cutsentence import Cut_Sentence

def Get_Statistics():
    
    Cut_Sentence()
    # 读取文件
    fn = open('/root/autodl-fs/Fengshenbang-LM/PromptRes/PromptData_Splited.txt', 'r', encoding='UTF-8')  # 打开文件
    string_data = fn.read()  # 读出整个文件
    fn.close()  # 关闭文件

    # 文本预处理
    pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式（空格等）
    string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

    # 文本分词
    seg_list_exact = jieba.cut(string_data, cut_all=False, HMM=True)  # 精确模式分词+HMM
    object_list = []

    for word in seg_list_exact:  # 循环读出每个分词
        object_list.append(word)  # 分词追加到列表

    number = 7
    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(number)  # 获取前number个最高频的词

    fileOut = open('/root/autodl-fs/Fengshenbang-LM/PromptRes/Statistics.txt', 'w', encoding='UTF-8')  # 创建文本文件；若已存在，则进行覆盖
    count = 0
    for TopWord, Frequency in word_counts_top:  # 获取词语和词频
        print(f'TopWord={TopWord} Frequency={Frequency}')
        if TopWord == ' ':
            continue
        for POS in jieba.posseg.cut(TopWord):  # 获取词性
            if count == number:
                break
            fileOut.write(TopWord + ' ' + str(Frequency) + '\n')  # 逐行写入str格式数据
            count += 1
    fileOut.close()  # 关闭文件
    #Transform_Form()

#Get_Statistics()