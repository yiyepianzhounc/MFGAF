import json
import pandas as pd
import os
import re
from tqdm import tqdm
from bart_score import BARTScorer
from sklearn.metrics import auc,roc_curve,roc_auc_score

# 初始化 BARTScorer
print("----------------------------------- 开始初始化 bart 模型 ------------------------------------------")
bartscorer = BARTScorer(device='cuda:0',checkpoint="facebook/bart-large-cnn")
print("----------------------------------- 结束初始化 bart 模型 ------------------------------------------")


# 读取 jsonl 文件
def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 将每一行的 JSON 字符串转换为字典
            data.append(json.loads(line.strip()))
    return data


# 读取 finance
file_path = 'finance_samples_gpt4i-mini.jsonl'  
finance_samples = read_jsonl(file_path)


def remove_chinese(text):
    # 使用正则表达式匹配所有中文字符并替换为空字符串
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return pattern.sub('', text)

# 不同的数据合并
question_full = []
human_answers_full = []
chatgpt_answers_full = []
human_answers_masked_full = []
chatgpt_answers_masked_full = []
human_answers_masked_fill_full = []
chatgpt_answers_masked_fill_full = []
human_answers_revised_full = []
chatgpt_answers_revised_full = []



for i, sample in tqdm(enumerate(finance_samples)):
    question = sample['question']
    human_answers = sample['human_answers']
    chatgpt_answers = sample['chatgpt_answers']
    human_answers_masked = sample['human_answers_masked']
    chatgpt_answers_masked = sample['chatgpt_answers_masked']
    human_answers_masked_fill = sample['human_answers_masked_fill']
    chatgpt_answers_masked_fill = sample['chatgpt_answers_masked_fill']
    human_answers_revised = sample['human_answers_revised']
    chatgpt_answers_revised = sample['chatgpt_answers_revised']

    # 去除中文
    human_answers_masked = remove_chinese(human_answers_masked)
    chatgpt_answers_masked = remove_chinese(chatgpt_answers_masked)
    human_answers_masked_fill = remove_chinese(human_answers_masked_fill)
    chatgpt_answers_masked_fill = remove_chinese(chatgpt_answers_masked_fill)

    # 存储
    question_full.append(question)
    human_answers_full.append(human_answers)
    chatgpt_answers_full.append(chatgpt_answers)
    human_answers_masked_full.append(human_answers_masked)
    chatgpt_answers_masked_full.append(chatgpt_answers_masked)
    human_answers_masked_fill_full.append(human_answers_masked_fill)
    chatgpt_answers_masked_fill_full.append(chatgpt_answers_masked_fill)
    human_answers_revised_full.append(human_answers_revised)
    chatgpt_answers_revised_full.append(chatgpt_answers_revised)



# 计算相似度
print("----------------------------------- 开始计算相似度 ------------------------------------------")
chatgpt_score = bartscorer.score(chatgpt_answers_revised_full, chatgpt_answers_full)
human_score = bartscorer.score(human_answers_revised_full, human_answers_full)
y_true = []
y_score = []
for i in range(0,len(chatgpt_score)):
    y_true.append(1)
    y_score.append(chatgpt_score[i])
for i in range(0,len(human_score)):
    y_true.append(0)
    y_score.append(human_score[i])

# 计算评估指标
auroc_score = roc_auc_score(y_true, y_score)
print("the auroc is:",auroc_score)




