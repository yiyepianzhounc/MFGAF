from transformers import pipeline
import torch

def reasoning_analysis(text1, text2):
    # 加载预训练的NLI模型
    nli_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    # 定义可能的标签
    labels = ["entailment", "contradiction", "neutral"]
    
    # 进行NLI分类
    result = nli_model(text2, candidate_labels=labels, hypothesis_template="This text is {}.")
    
    # 获取entailment的概率作为一致性分数
    consistency_score = result['scores'][result['labels'].index('entailment')]
    
    return consistency_score

def calculate_consistency(paragraph1, paragraph2):
    # 计算双向的一致性分数
    score1 = reasoning_analysis(paragraph1, paragraph2)
    score2 = reasoning_analysis(paragraph2, paragraph1)
    
    # 取平均值作为最终的一致性分数
    final_score = (score1 + score2) / 2
    
    return final_score

# 使用示例
paragraph1 = "Input your first paragraph here."
paragraph2 = "Input your second paragraph here."

consistency_score = calculate_consistency(paragraph1, paragraph2)
print(f"推理共振分析的一致性分数: {consistency_score:.4f}")
