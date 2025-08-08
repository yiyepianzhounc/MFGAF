import pandas as pd
import json
import os
from tqdm import tqdm
import time
import json

# 读取 jsonl 文件
def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 将每一行的 JSON 字符串转换为字典
            data.append(json.loads(line.strip()))
    return data


import openai
import requests

# 设置 API 密钥
openai.api_key = 'sk-wZh36lLFrW3cPYfA401fBd6859D34a47A26dDdDdC210B3A2'

# 自定义 API 基础 URL
openai.api_base = 'https://www.gptapi.us/v1/chat/completions'

# 定义调用函数
def call_gpt4o(prompt, model="gpt-4o-mini"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']



# 1、读取数据
# 读取 finance
file_path = 'finance.jsonl'  
finance = read_jsonl(file_path)

# 读取 revised_chatgpt_finance
file_path = 'revised_chatgpt_finance.txt'  
revised_chatgpt_finance = read_jsonl(file_path)

# 读取 revised_human_finance
file_path = 'revised_human_finance.txt'  
revised_human_finance = read_jsonl(file_path)


# 2、随机选择一部分 mask
import re
import random

def split_sentences(text):
    # 使用正则表达式根据英文标点符号分割句子
    sentences = re.split(r'(?<=[.!?]) +', text)
    # 去除空字符串
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def mask_sentences(text, mask_token="[MASK]"):
    sentences = split_sentences(text)
    # 计算需要 mask 的子句子数量
    num_to_mask = max(1, len(sentences) // 2)
    # 随机选择要 mask 的子句子
    masked_indices = random.sample(range(len(sentences)), num_to_mask)
    # 进行 mask
    for i in masked_indices:
        sentences[i] = mask_token
    # 重新组合成完整的句子
    masked_text = ' '.join(sentences)
    return masked_text



def fill_mask_by_gpt(question, text_masked):
    """ 根据 question 对 mask 后的句子进行填充 """

    prompt = f"""
        请你扮演一个文本信息处理人员，你需要根据我下面的要求对原始句子进行填充:
        （1）填充mask：根据输入的 question 和 text_masked，对 text_masked 中的 [MASK] 进行填充；
        （2）填充逻辑：需要尽量上下文一致，而且需要与输入的 question 直接相关；
        （3）填充数量：每个 [MASK] 代表一个小句，即英文中用 ',' 分隔两个小句，而不是用 '.' 分隔两个小句；
        （4）输出：你只需要输出填充后的字符串，不需要其他任何无关的内容；

        下面是一个样例:
        【input】:
            question: Historical P/E ratios of small-cap vs. large-cap stocks?
            
            text_masked: There is most likely an error in the WSJ's data. [MASK] [MASK] Good catch, though! E-mail WSJ, perhaps they will be grateful.
            
        【output】:
            There is most likely an error in the WSJ's data. Small-cap stocks typically have higher P/E ratios than large-cap stocks. and the discrepancy might explain the inconsistency. Good catch, though! E-mail WSJ, perhaps they will be grateful.

        你需要仔细理解我上面的要求，帮我对 mask 后的句子进行填充。
        下面我将给你我的输入，你只需要给我填充后的字符串即可，切记不需要任何其他无关的内容。

        【input】:
            question: {question}

            text_masked: {text_masked}

        【output】:
            
    """
    try:
        llm_res = call_gpt4o(prompt)
    except:
        time.sleep(0.5)
        llm_res = 'error'

    return llm_res



def revise_by_gpt(question, text_masked):
    """ 根据 question 对 原始句子 进行改写 """

    prompt = f"""
        请你扮演一个文本信息处理人员，你需要根据我下面的要求对原始句子进行改写:
        （1）改写逻辑：需要尽量上下文一致，而且需要与输入的 question 直接相关；
        （2）篇幅：需要与输入的 text_masked 篇幅基本上一致，不要过多增加或者减少；
        （3）输出：你只需要输出填充后的字符串，不需要其他任何无关的内容；

        你需要仔细理解我上面的要求，帮我对原始的句子进行改写。
        下面我将给你我的输入:

        输入为:
            question: {question}

            text_masked: {text_masked}

        你只需要给我改写后的句子即可，切记不需要任何其他无关的内容。
        你改写后的句子为:
            
    """
    try:
        llm_res = call_gpt4o(prompt)
    except:
        time.sleep(0.5)
        llm_res = 'error'

    return llm_res




def save_to_jsonl(data, filename, mode='w', clear_before_write=False):
    """
    将 Python 列表存储为 JSON Lines 文件。

    参数:
        data (list): 要存储的 Python 列表，列表中的每个元素是一个字典。
        filename (str): 目标文件名（如 'data.jsonl'）。
        mode (str): 文件写入模式，默认为 'w'（覆盖写入）。
                    如果需要追加写入，可以设置为 'a'。
        clear_before_write (bool): 是否在写入前清空文件内容，默认为 False。
    """
    if clear_before_write and mode == 'w':
        # 清空文件内容
        with open(filename, 'w', encoding='utf-8') as f:
            f.truncate(0)  # 清空文件

    with open(filename, mode, encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)  # ensure_ascii=False 支持非 ASCII 字符
            f.write('\n')  # 每个 JSON 对象后写入换行符





samples_full = []


for i, input_dict in tqdm(enumerate(finance)):

    question = input_dict['question']
    human_answers = input_dict['human_answers']
    chatgpt_answers = input_dict['chatgpt_answers']

    if type(human_answers) == list:
        human_answers = human_answers[0]
    if type(chatgpt_answers) == list:
        chatgpt_answers = chatgpt_answers[0]

    # 生成 mask
    human_answers_masked = mask_sentences(human_answers)
    chatgpt_answers_masked = mask_sentences(chatgpt_answers)

    # 填充 mask 的
    human_answers_masked_fill = fill_mask_by_gpt(question, human_answers_masked)
    chatgpt_answers_masked_fill = fill_mask_by_gpt(question, chatgpt_answers_masked)

    
    # 获得重写的
    human_answers_revised = revised_human_finance[i][str(i)]
    chatgpt_answers_revised = revised_chatgpt_finance[i][str(i)]


    # 自己重写
    human_answers_revised_by_gpt = revise_by_gpt(question, human_answers)
    chatgpt_answers_revised_by_gpt = revise_by_gpt(question, chatgpt_answers)


    # 存储
    sample = {
        'question': question,
        'human_answers': human_answers,
        'chatgpt_answers': chatgpt_answers,
        'human_answers_masked': human_answers_masked,
        'chatgpt_answers_masked': chatgpt_answers_masked,
        'human_answers_masked_fill': human_answers_masked_fill,
        'chatgpt_answers_masked_fill': chatgpt_answers_masked_fill,
        'human_answers_revised': human_answers_revised,
        'chatgpt_answers_revised': chatgpt_answers_revised,
        'human_answers_revised_by_gpt': human_answers_revised_by_gpt,
        'chatgpt_answers_revised_by_gpt': chatgpt_answers_revised_by_gpt
    }
    samples_full.append(sample)


    # v2 是包括了自己使用 gpt 重写
    save_to_jsonl(samples_full, 'finance_samples_gpt4i-mini_v2.jsonl')


    







