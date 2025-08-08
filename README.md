# MFGAF: Multi-faceted Granular Analysis Framework for LLM-Generated Text Detection

This repository contains the official implementation for the paper: **"MFGAF: Multi-faceted Granular Analysis Framework for LLM-Generated Text Detection"**.

Our framework introduces a novel zero-shot approach for detecting LLM-generated text by leveraging dual perspectives (Rewriting and Completion) and a multi-granular textual analysis across semantic, syntactic, lexical, and reasoning dimensions.

<!-- You can add your framework diagram here -->
<!-- ![Framework Overview](framework_diagram.png) -->

## 1. Dataset

This study utilizes the public benchmark dataset released with the paper:

> **Raidar: GeneRative AI Detection viA Rewriting**
>
> Chengzhi Mao, Carl Vondrick, Hao Wang, and Junfeng Yang. In *ICLR 2024*.

We sincerely thank the authors of Raidar for making their data publicly available.

#### Data Collection and Annotation

As we use an existing dataset, all details regarding data collection and annotation can be found in the original Raidar paper. The dataset covers six domains: News, Creative Writing, Student Essays, Code, Reviews, and Abstracts. The texts were generated using models like GPT-3.5-turbo and GPT-4.

#### Data Usage

To use the dataset for this project, please follow these steps:
1.  Visit the official Raidar repository: [https://github.com/cvlab-columbia/RaidarLLMDetect](https://github.com/cvlab-columbia/RaidarLLMDetect)
2.  Follow their instructions to download the dataset.
3.  Place the downloaded data files into the directory of this project.

#### Data Sample

A typical data entry from the dataset is a JSON object containing a question and various corresponding human- and machine-generated texts. The structure of our project's preprocessed data is as follows:

```json
{
  "question": "Where can I lookup accurate current exchange rates for consumers?",
  "human_answers": "Current and past FX rates are available on Visa's website...",
  "chatgpt_answers": "There are several websites and resources that provide accurate and current exchange rates...",
  "human_answers_masked": "[MASK] Note that it may vary by country...",
  "chatgpt_answers_masked": "[MASK] [MASK] You can typically find this information...",
  "human_answers_masked_fill": "You can lookup accurate current exchange rates for consumers on financial news websites...",
  "chatgpt_answers_masked_fill": "Here is the filled text:\n\nYou can typically find this information...",
  "human_answers_revised": "\n\nVisa's website provides both current and past FX rates...",
  "chatgpt_answers_revised": "\n\nConsumers have access to various websites and resources..."
}
