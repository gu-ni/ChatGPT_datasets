# %%
import os
import re
import json

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


def merge_narrative_and_coding(narrative: str, coding: str) -> str:
    return f"### Narrative format:\n{narrative}\n\n### Coding Test format:\n{clean_text(coding)}"


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
lcb_path = "/home/work/users/PIL_ghj/LLM/datasets/live-code-bench/test6.jsonl"

# 입력 파일 경로
input_jsonl_path = "/home/work/users/PIL_ghj/LLM/datasets/ChatGPT/LiveCodeBench/test6_narrative_by_gpt.jsonl"

# 출력 파일 경로
output_path_name = "LiveCodeBench"  # HumanEval LiveCodeBench CodeForces

# 파일명
file_name = "test6_merged.jsonl" # humaneval_narrative_by_gpt_test.jsonl test6_narrative_by_gpt_test.jsonl


output_path = f"/home/work/users/PIL_ghj/LLM/datasets/ChatGPT/{output_path_name}"
os.makedirs(output_path, exist_ok=True)

output_jsonl_path = os.path.join(output_path, file_name)

# 중복 체크
existing_ids = load_existing_question_ids(output_jsonl_path)

# 입력 파일 처리
with open(input_jsonl_path, "r", encoding="utf-8") as infile, \
    open(lcb_path, "r", encoding="utf-8") as lcb, \
    open(output_jsonl_path, "a", encoding="utf-8") as outfile:  # append 모드로 열기
    
    for i, line in enumerate(infile):
        try:
            problem = json.loads(line)
            qid = problem.get("question_id")
            print(f"\n[Logging] Starting {i}-th Problem ({qid})...")
            # if qid in existing_ids:
            #     print(f"[Logging] Skipping already processed question_id: {qid}")
            #     continue
            
            for lcb_problem in lcb:
                try:
                    lcb_problem = json.loads(lcb_problem)
                    if lcb_problem["question_id"] and lcb_problem["question_id"] == qid:
                        narrative = problem.get("question_content")
                        coding_test = lcb_problem.get("question_content")
                        
                        problem["question_content"] = merge_narrative_and_coding(narrative, coding_test)
                        break
                except Exception as e:
                    print(f"Error processing a problem: {e}")
                    continue
                    
            outfile.write(json.dumps(problem, ensure_ascii=False) + "\n")
            existing_ids.add(qid)

        except Exception as e:
            print(f"Error processing a problem: {e}")
            continue
        
# %%
