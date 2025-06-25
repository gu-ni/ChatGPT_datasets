# %%
import os
import re
import json
from datasets import load_dataset

# %%

def normalize_confusables(text: str) -> str:
    replace_map = {
        "\u2009": " ",   # thin space → space
        "\u00D7": "x",   # multiplication sign → x
        "\u2013": "-",   # en dash → hyphen
        "\u2212": "-",
        "\u2217": "*",
        "\u0421": "C",
    }
    for key, val in replace_map.items():
        text = text.replace(key, val)
    return text


def clean_text(text: str) -> str:
    if not text:
        return ""
    # $$$...$$$ 제거
    text = re.sub(r"\$\$\$(.*?)\$\$\$", r"\1", text)
    # $...$ 제거
    text = re.sub(r"\$(.*?)\$", r"\1", text)
    # ~ 제거 (띄어쓰기 대체)
    text = re.sub(r"~", " ", text)
    # 연속 공백 정리
    text = re.sub(r"[ \t]+", " ", text)
    # 3줄 이상 연속 줄바꿈 → 2줄로 축소
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    text = normalize_confusables(text)
    return text.strip()


def convert_examples(examples:list) -> str:
    parts = []

    # Sample Input/Output 추가
    for idx, ex in enumerate(examples):
        input_str = clean_text(ex.get("input", ""))
        output_str = clean_text(ex.get("output", ""))
        parts.append(f"\n\nSample Input {idx + 1}\n\n{input_str}\n\nSample Output {idx + 1}\n\n{output_str}")

    return "\n".join(parts)


# 기존 출력 파일에서 이미 처리한 ID 수집
def load_existing_question_ids(path):
    if not os.path.exists(path):
        return set()
    existing_ids = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                qid = obj.get("question_id")
                if qid:
                    existing_ids.add(qid)
            except Exception:
                continue
    return existing_ids

# %%
codeforces_dataset = load_dataset("open-r1/codeforces", split="train", name='verifiable')

filtered_codeforces_dataset = []
for x in codeforces_dataset:
    if x["description"] and x["rating"] and x["input_format"] and x["output_format"] \
    and len(x["description"]) <= 1000 and x["rating"] > 3000\
    and "multiple test" not in x["input_format"] and not x["generated_checker"] \
    and x["examples"] and len(x["official_tests"]) <= 20:
        filtered_codeforces_dataset.append(x)

del codeforces_dataset


# 입력 파일 경로
input_jsonl_path = "/home/work/users/PIL_ghj/LLM/datasets/ChatGPT/CodeForces/codeforces_challenging_narrative_by_gpt.jsonl"
# "/home/work/users/PIL_ghj/LLM/datasets/human-eval/data/HumanEval_in_lcb_format.jsonl"
# "/home/work/users/PIL_ghj/LLM/datasets/live-code-bench/test6.jsonl"

# 출력 파일 경로
output_path_name = "CodeForces"  # HumanEval LiveCodeBench CodeForces

# 파일명
file_name = "codeforces_challenging_narrative_by_gpt_with_io.jsonl" # humaneval_narrative_by_gpt_test.jsonl test6_narrative_by_gpt_test.jsonl


output_path = f"/home/work/users/PIL_ghj/LLM/datasets/ChatGPT/{output_path_name}"
os.makedirs(output_path, exist_ok=True)

output_jsonl_path = os.path.join(output_path, file_name)

# 중복 체크
existing_ids = load_existing_question_ids(output_jsonl_path)

# 입력 파일 처리
with open(input_jsonl_path, "r", encoding="utf-8") as infile, \
    open(output_jsonl_path, "a", encoding="utf-8") as outfile:  # append 모드로 열기
    
    for i, line in enumerate(infile):
        try:
            problem = json.loads(line)
            qid = problem.get("question_id")
            print(f"\n[Logging] Starting {i}-th Problem ({qid})...")
            if qid in existing_ids:
                print(f"[Logging] Skipping already processed question_id: {qid}")
                continue
            
            for original_format_sample in filtered_codeforces_dataset:
                if original_format_sample["id"] and original_format_sample["id"] == qid \
                and original_format_sample["examples"]:
                    examples = original_format_sample["examples"]
                    examples_str = convert_examples(examples)
                    
                    question_content = problem.get("question_content")
                    problem["question_content"] = question_content + examples_str
                    break
            
            outfile.write(json.dumps(problem, ensure_ascii=False) + "\n")
            existing_ids.add(qid)

        except Exception as e:
            print(f"Error processing a problem: {e}")
            continue
        
# %%


