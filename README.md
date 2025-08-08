# MFGAF: Multi-faceted Granular Analysis Framework for LLM-Generated Text Detection

This repository contains the official implementation for the paper: **"MFGAF: Multi-faceted Granular Analysis Framework for LLM-Generated Text Detection"**.

Our framework introduces a novel zero-shot approach for detecting LLM-generated text by leveraging dual perspectives (Rewriting and Completion) and a multi-granular textual analysis across semantic, syntactic, lexical, and reasoning dimensions.

<!-- You can add your framework diagram here -->
<!-- ![Framework Overview](framework_diagram.png) -->

## 1. Dataset

This study utilizes the public benchmark dataset released with the paper:

> **Raidar: GeneRative AI Detection viA Rewriting**
>
> Chengzhi Mao, Carl Vondrick, and Junfeng Yang. In *ICLR 2024*.

We sincerely thank the authors of Raidar for making their data publicly available.

#### Data Collection and Annotation

As we use an existing dataset, all details regarding data collection and annotation can be found in the original Raidar paper. The dataset covers six domains: News, Creative Writing, Student Essays, Code, Reviews, and Abstracts. The texts were generated using models like GPT-3.5-turbo and GPT-4.

#### Data Usage

To use the dataset for this project, please follow these steps:
1.  Visit the official Raidar repository: [https://github.com/chengzhi-mao/Raidar](https://github.com/chengzhi-mao/Raidar)
2.  Follow their instructions to download the dataset.
3.  Place the downloaded data files into the `data/` directory of this project.

#### Data Sample

A typical data entry from the dataset is structured as a JSON object, containing both a human-written text and its corresponding machine-generated version. For example:

```json
{
  "domain": "News",
  "human_text": "The prime minister announced new environmental policies today, focusing on renewable energy...",
  "machine_text": "New environmental regulations centered on renewable energy sources were unveiled by the prime minister today...",
  "label": 1 // 0 for human, 1 for machine
}
