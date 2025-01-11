
import json

data = json.load(open('aug-data/aug_discourse_edu.json'))
for item in data:
    # dialogue texts
    dialogue = item['dialog']
    print(dialogue)
    # [{'turn': 0, 'utterance': '您 好 ， 请问 您 有 什么 需要 帮助 的 吗 ？', 'speaker': 'Q'}, {'turn': 1, 'utterance': '祝 您 心情 一直 如此 好', 'speaker': 'Q'}, ...]
    # 'turn' 表示第几轮对话，'utterance' 表示对话内容，'speaker' 表示说话人的角色
    # dialogue relationships
    print(item['relationship'])
    # [['0-2', 'subj', '0-1'], ['0-2', 'punc', '0-3'], ['0-6', 'subj', '0-5'], ...]
    # '0-2' 表示第 0 轮对话的第 2 个词（发射箭头的词），'subj' 表示主语，'0-1' 表示第 0 轮对话的第 1 个词（接收箭头的词），'punc' 表示标点符号，'0-3' 表示第 0 轮对话的第 3 个词，...
    # 注意词的下标从1开始，0表示虚根
    break