from collections import Counter

text = '''
1	刘就按	48152619121215383X	6228480848817471870	中国农业银行 - 广西北流市支行
2	罗的	951981199911183929	6230388183018295155	东莞农村商业银行 - 东莞市大岭山镇新塘支行
3	何打翻	852526197202013989	6231988800028851980	东莞农村商业银行 - 东莞市大岭山镇新塘支行
4	刘的	460934199710083974	6230388810128295700	东莞农村商业银行 - 东莞市大岭山镇新塘支行
5	何就去	35252619760410394X	6228480791396722115	中国农业银行 - 广西北流市支行
6	丘到	152456197507153953	6218760849563178876	中国农业银行 - 广西北流市支行
'''

text = '''
Vance-liu@139.com (ANPPQ4) - A
Joey-liu@139.com (ANPIHQ) - B
Aaron-liu@139.com (ANPIP4) + C
JC-liu@139.com (ANPIQT) - D
'''

text = '''
刘盛郁	45252619721215393X	6228480848823771870	中国农业银行 - 广西北流市支行
罗艳珍	450981199910183929	6230388810018295155	东莞农村商业银行 - 东莞市大岭山镇新塘支行
何传清	452526197204113989	6230388800028851980	东莞农村商业银行 - 东莞市大岭山镇新塘支行
刘亮伟	450981199710083974	6230388810018295700	东莞农村商业银行 - 东莞市大岭山镇新塘支行
何海英	45252619760410394X	6228480841396722115	中国农业银行 - 广西北流市支行
丘先冀	452526197507153953	6213360849903116876	中国农业银行 - 广西北流市支行
'''

# print(text.replace('\t', '\\t'))
import re
import string
from pandas import DataFrame

whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace


# TODO 统计每行的table符号数量，空格数量，punctuatioin符号数量
# TODO 多space的时候，替换成一个再处理？
# print(re.sub(whitespace, ',', text))

def split_string_by_indices(s: str, indices: list):
    result = []
    start = 0
    idx_list = []
    for index in sorted(indices):
        result.append(s[start:index])
        # idx_list.append([start, index])
        idx_list.append(index)
        start = index
    result.append(s[start:])
    # idx_list.append([start, len(s)])
    idx_list.append(len(s))
    result = [s for s in result if s]
    return result, idx_list


def find_indices(s, char):
    return [i for i, c in enumerate(s) if c == char]


def analyze_string(text):
    space_delimiters = '\t '  # common delimiters

    original_text = text
    text = text.strip()

    first_row = text.split('\n')[0]
    common_set = set(first_row) & set(space_delimiters + punctuation)

    last_row_dct = {}
    for row in text.split('\n'):
        # TODO 剪枝策略
        row_dct = {ch: row.count(ch) for ch in common_set}
        if last_row_dct:
            diff = Counter(last_row_dct) - Counter(row_dct)
            for k, v in diff.items():
                common_set.remove(k)
                row_dct.pop(k)

        last_row_dct = row_dct

    data = []
    idxs = []
    delimiters = list(last_row_dct.keys())
    print(f'delimiters: {delimiters}')

    if '\t' in delimiters:
        delimiters = ['\t']

    elif ' ' in delimiters:
        delimiters = [' ']

    for row in text.split('\n'):
        row_idx = []
        for ch in delimiters:
            idx = find_indices(row, ch)
            row_idx += idx
            row_idx += [i + 1 for i in idx]

        res, idx_list = split_string_by_indices(row, row_idx)
        data.append(res)
        idxs.append(idx_list)
        print('-' * 20)

    for row in data:
        print(row)

    return data, idxs


if __name__ == '__main__':
    # TODO extract automatically phone,email,link,ip,datetime
    # TODO 自动生成代码（或处理逻辑）
    # TODO 支持插件（写一段代码，定义插件按钮）
    # TODO 可以拖动文本，来修改
    pass
    # TODO 显示出分割情况
    # TODO 双击选中分割的某一列
    analyze_string(text)

    print(len('Vance-liu@139.com (ANPPQ4) - A'))