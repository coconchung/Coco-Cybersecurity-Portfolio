#!/usr/bin/env python3
import itertools
import hashlib
import re
import time
from pathlib import Path

SPECIALS_C = "!@#$%&*"
MAXC = 20

EMAIL_DATASET = "email_md5_dataset.txt"
KEYWORDS = "keywords.txt"


def loading_dataset_keywords():
    # Loading dataset
    with open(EMAIL_DATASET, "r", encoding="utf-8", errors="ignore") as file:
        lines = [line.strip().split(",", 1) for line in file if "," in line]

    e_md5h = [(e.strip(), md5h.strip().lower())
             for e, md5h in lines
             if re.fullmatch(r"[0-9a-f]{32}", md5h.strip().lower())]

    all_hashes = {md5h: e for e, md5h in e_md5h}

    # Loading keywords
    all_words = []
    with open(KEYWORDS, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            raw_line = line.strip()
            if not raw_line:
                continue 
            stripped_line = raw_line.lower()
            stripped_line = re.sub(r"[^a-z0-9]", "", stripped_line)
            if stripped_line:
                all_words.append(stripped_line)
    unique_words = []
    seen_words = set()
    for i in all_words:
        if i not in seen_words:
            unique_words.append(i)
            seen_words.add(i)

    # Returning dataset and keywords that have been loaded
    return all_hashes, unique_words

def all_combinations(words):
    seen_combos = set()

    for r in range(1, min(4, len(words)) + 1):
        for combo in itertools.permutations(words, r):
            base_layout = "".join(combo)

            # 4 cases based on the special character
            # 1. This is the basic base
            if 0 < len(base_layout) < MAXC and base_layout not in seen_combos:
                seen_combos.add(base_layout)
                yield base_layout

            # 2. This is the one with the special character at the start
            for special in SPECIALS_C:
                chosen_combo = special + base_layout
                if 0 < len(chosen_combo) < MAXC and chosen_combo not in seen_combos:
                    seen_combos.add(chosen_combo)
                    yield chosen_combo

            # 3. This is the one with the special character at the end
            for special in SPECIALS_C:
                chosen_combo = base_layout + special
                if 0 < len(chosen_combo) < MAXC and chosen_combo not in seen_combos:
                    seen_combos.add(chosen_combo)
                    yield chosen_combo

            # 4. This is the one with the special character in the middle
            if r > 1:
                first = combo[0]
                rest = "".join(combo[1:])
                for special in SPECIALS_C:
                    chosen_combo = first + special + rest
                    if 0 < len(chosen_combo) < MAXC and chosen_combo not in seen_combos:
                        seen_combos.add(chosen_combo)
                        yield chosen_combo


def main():
    # Loading the dataset and keywords
    hashes, words = loading_dataset_keywords()
    start_time = time.time()
    total_permutations = 0

    # Finding all the possible password combinations based of the words
    for password in all_combinations(words):
        total_permutations += 1 # 3. Increment counter
        chosen_md5h = hashlib.md5(password.encode()).hexdigest()

        # When the hash exists in the database then print the required information
        if chosen_md5h in hashes:
            end_time = time.time()
            duration = end_time - start_time
            hps = total_permutations / duration if duration > 0 else 0
            
            print("="*30)
            print(f"Match found in {duration:.4f} seconds")
            print(f"Total Permutations Tested: {total_permutations}")
            print(f"Throughput: {hps:.2f} hashes/sec")
            print(f"Email: {hashes[chosen_md5h]}, Password: {password}")
            print("="*30)
            return

    print("There are no matches")

if __name__ == "__main__":
    main()
