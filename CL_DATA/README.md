
## 数据集说明
```
data: 原始数据集
|- dialog: 对话数据集
--|- train: 训练集
--|- test: 测试集
|- syntax: 句法树数据集（conll格式）
--|- ...

aug-data: 增强数据集
- aug_word_edu.json: 对EDUs进行word-level的增强
- aug_word_uttr.json: 对utterances进行word-level的增强
- aug_syntax_edu.json: 对EDUs进行syntax-level的增强
- aug_syntax_uttr.json: 对utterances进行syntax-level的增强
- aug_discourse_edu.json: 对EDUs进行discourse-level的增强
- aug_discourse_uttr.json: 对utterances进行discourse-level的增强

aug-data-extend: 利用LLM的随机性多次生成的增强数据集 (all for utterances)
- aug_by_word_x.json:
- aug_by_syntax_x.json:
```

## 数据集格式说明
所有json文件均为字典列表，每个元素为一个对话，对话由多个utterance组成
```
[
    {
        "id": 10374,
        "dialog": [
            {
                "turn": 0,   # 第几轮对话，从0开始
                "utterance": "请 您 稍 等 ， 正在 为 您 确认 此前 咨询 内容 。",   # 文本内容，词以空格为分隔
                "speaker": "A"   # 说话人
            },
            ...
        ],
        "relationship": [
            [
                "0-0",     # 发射词，i_j, i是utterance的index，j是词的index，其中j=0代表当前utterance的虚根
                "root",      #  关系
                "0-1"    # 接收词，下标与发射词相同
            ],
            ...
        ]
    }
]
```

## 关系说明
### 句法关系
| Label        | Meaning                |
|--------------|------------------------|
| root         | root                   |
| sasubj-obj   | same subject, object    |
| sasubj       | same subject            |
| dfsubj       | different subject       |
| subj         | subject                |
| subj-in      | innersubject           |
| obj          | object                 |
| pred         | predicate              |
| att          | attribute modifier      |
| adv          | adverbial modifier      |
| cmp          | complement modifier     |
| coo          | coordination           |
| pobj         | preposition object      |
| iobj         | indirect-object        |
| de           | de-construction        |
| adjct        | adjunct                |
| app          | appellation            |
| exp          | explanation            |
| punc         | punctuation            |
| frag         | fragment               |
| repet        | repetition             |

关系说明详见CODT句法树库：
http://hlt.suda.edu.cn/index.php/CODT

### 篇章关系
| Label    | Meaning             |
|----------|---------------------|
| attr     | attribution，归属，直接或间接报告的事情，一般使用了认知谓词，可以利用说、报告、感觉、想、希望...等词语进行辨别         |
| bckg     | background，背景（事件的背景，不强调因果）          |
| cause    | cause，因果               |
| comp     | comparison，比较（重点关注大小、数字等比较）          |
| cond     | condition，条件（强调某个事件发生的条件）           |
| cont     | contrast，对比（强调转折）            |
| elbr     | elaboration，阐述（最一般普遍的关系）          |
| enbm     | enablement，使能（驱动、促进、请求、激励某个将来事件发生）          |
| eval     | evaluation，评估（对某个事件发表评价）          |
| expl     | explanation，解释 （对某个事物的例证、解释、辩驳、释因）       |
| joint    | joint，联合（强调多个事物的枚举，没有明确时序或因果等关系）               |
| manner   | manner-means，方法（强调手段）          |
| rstm     | restatement，重述（强调重述）          |
| temp     | temporal，时序（强调时间上的先后）            |
| tp-chg   | topic-change，主题转变         |
| prob-sol | problem-solution，从问题到提出解决方案    |
| qst-ans  | question-answer，从提出疑问到回答     |
| stm-rsp  | statement-response，对陈述进行回复  |
| req-proc | requirement-process，对需求进行处理 |