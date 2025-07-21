import json
from pathlib import Path

qa_balanced = 'valid_grader/all_mc_qas.json'
qa_generated = 'valid/_captions.json'

def main():
    qa_b = json.load(open(Path(__file__).parent / qa_balanced))
    qa_g = json.load(open(Path(__file__).parent / qa_generated))

    print(f"Number of captions golden: {len(qa_b)}")
    print(f"Number of captions generated: {len(qa_g)}")

    # Index generated captions by image_file for fast lookup
    generated_by_image = {}
    for qb in qa_g:
        image_file = qb["image_file"]
        if image_file not in generated_by_image:
            generated_by_image[image_file] = []
        generated_by_image[image_file].append(qb["caption"])

    count_missing = 0
    count_correct = 0

    for idx, qa in enumerate(qa_b):
        image_file = qa["image_file"]
        correct_caption = qa["candidates"][qa["correct_index"]]

        if image_file not in generated_by_image:
            print(f"Not found: {qa}")
            count_missing += 1
            continue

        if correct_caption in generated_by_image[image_file]:
            count_correct += 1
        else:
            print(f"Wrong answer for image {image_file}:\nExpected: {correct_caption}\nGenerated: {generated_by_image[image_file]}")

    print(f"\nNumber of missing images: {count_missing}")
    print(f"Number of correct caption matches: {count_correct} out of {len(qa_b)}")

main()
