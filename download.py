""" 加载模型 """
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
from modelscope import snapshot_download
model_dir = snapshot_download("AI-ModelScope/bge-large-en-v1.5", cache_dir='pretrain_models', revision='master') # 加载模型

from sentence_transformers import SentenceTransformer
model = SentenceTransformer(model_dir)

