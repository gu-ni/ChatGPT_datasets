# %%
import json


def convert_test_cases(test_cases_list: list) -> str:    
    parts = []

    # Sample Input/Output 추가
    for idx, test_cases in enumerate(test_cases_list):
        input_str = test_cases.get("input", "")
        output_str = test_cases.get("output", "")
        parts.append(f"\n\nSample Input {idx + 1}\n\n{input_str}\n\nSample Output {idx + 1}\n\n{output_str}")

    return "\n".join(parts)

def add_io(task: dict) -> dict:    
    question_content = task.get("question_content")
    public_test_cases = task.get("public_test_cases")
    
    test_cases_list = json.loads(public_test_cases)
    test_cases_str = convert_test_cases(test_cases_list)
    
    task["question_content"] = question_content + test_cases_str
    
    return task

# %%

input_jsonl_path = "/home/work/users/PIL_ghj/LLM/datasets/ChatGPT/LiveCodeBench/test6_narrative_by_gpt.jsonl"
output_jsonl_path = "/home/work/users/PIL_ghj/LLM/datasets/ChatGPT/LiveCodeBench/test6_narrative_by_gpt_with_io.jsonl"

with open(input_jsonl_path, "r", encoding="utf-8") as infile, \
    open(output_jsonl_path, "a", encoding="utf-8") as outfile:  # append 모드로 열기
    
    for i, line in enumerate(infile):
        try:
            task = json.loads(line)
            task = add_io(task)
            outfile.write(json.dumps(task, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Error processing a problem: {e}")
            continue

# %%
print("In the heart of the ancient City of Multiplica, there stands a grand Hall of Tables—a marvel famed for its enormous mosaic floor. This floor is arranged as a perfect square, nine tiles wide and nine tiles deep, with each tile inscribed by the artisans with a number: the product of its row and column numbers. The rows and columns are both numbered from one to nine, so every tile in the hall displays the result of multiplying its row’s number by its column’s number. Visitors marvel at the intricate repetition and the patterns that form across the 81 tiles.\n\nThe city’s scholars uphold certain traditions regarding the Hall. They insist that each tile’s value be honored as many times as it appears; if a number is repeated among the tiles, each instance must be counted individually in any tally. There is, however, a unique custom: on certain festival days, the city’s leader announces a forbidden number—a specific value between one and eighty-one, inclusive. On that day, all calculations and ceremonies in the Hall must ignore the forbidden number wherever it appears, treating those tiles as if they bear no value at all. If the forbidden number does not appear on any tile, the scholars proceed unimpeded, summing every value in the Hall.\n\nOn such a day, the challenge is set forth to the city’s mathematicians: “Given the forbidden number, determine the grand sum of all the values on the Hall’s mosaic, save for those tiles where the forbidden number appears. Each tile is counted in the sum according to its own value, and repetitions are respected. If the forbidden number is absent, the entire mosaic’s sum is to be reported. If the forbidden number is present, its contribution is omitted from every tile where it appears.”\n\nFor this ritual, participants are given a single scroll naming the day’s forbidden number. Their task is to announce, with clarity and precision, the sum of all values on the Hall’s tiles except those where the forbidden number is found. The scroll is presented in this manner: a solitary integer, inscribed upon it, between one and eighty-one. After careful calculation, the mathematician proclaims a single number—the sum as decreed by the festival’s rules.\n\nLet us recount three festival days as recorded in the city’s annals:  \nOn the day when the forbidden number was one, only the tile at the very first row and first column bore this value. The mathematicians summed every other value, arriving at the total of two thousand and twenty-four.  \nOn another day, when eleven was declared forbidden, not a single tile bore this number in the mosaic. Therefore, the sum of all the tiles, two thousand and twenty-five, was announced.  \nOn a third occasion, when twenty-four was forbidden, the scholars found all tiles showing this value and omitted their contributions, yielding a final sum of one thousand nine hundred and twenty-nine.\n\nThus, the customs of Multiplica endure, and the Hall’s mosaic continues to challenge and inspire each new generation of thinkers.\n\nSample Input 1\n\n1\n\nSample Output 1\n\n2024\n\n\nSample Input 2\n\n11\n\nSample Output 2\n\n2025\n\n\nSample Input 3\n\n24\n\nSample Output 3\n\n1929")


# %%
