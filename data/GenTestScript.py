import json
from pathlib import Path

qa_balanced = 'valid_grader/balanced_qa_pairs.json'
qa_generated = 'valid/_qa_pairs.json'

def main():

    qa_b = json.load(open(Path(__file__).parent / qa_balanced))
    qa_g = json.load(open(Path(__file__).parent / qa_generated))

    print(f"Number of qa_pairs golden: {len(qa_b)}")
    print(f"Number of qa_pairs generated: {len(qa_g)}")

    #check that every pair from golden is in generated
    count = 0
    correct = 0
    for idx, qa in enumerate(qa_b):
        found = False
        for qb in qa_g:
            if (qa["question"] == qb["question"] and qa["image_file"] == qb["image_file"]):
                found = True
                if qb["answer"] == qa["answer"]:
                    correct += 1
                else:
                    print(f"Wrong answer: {qa}     \nCorrect answer: {qb['answer']}")
                    break
        if not found:
            print("Not found: ", qa)
            count += 1
    print(f"Number of qa pairs missing: {count} Correct: {correct}")

main()
