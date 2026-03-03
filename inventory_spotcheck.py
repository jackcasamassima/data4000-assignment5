# inventory_spotcheck.py
# DATA 4000 — Assignment 5 (Exercise 2)

import requests


def compute_seed(student_key: str) -> int:
    return sum(ord(ch) for ch in student_key.strip())


def prompt_nonempty_sku() -> str:
    while True:
        sku = input("SKU: ").strip()
        if sku.upper() == "DONE":
            return "DONE"
        if sku == "":
            print("Invalid input. Please try again.")
            continue
        return sku


def prompt_on_hand() -> int:
    while True:
        raw = input("On hand: ").strip()
        try:
            val = int(raw)
            if val < 0:
                print("Invalid input. Please try again.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please try again.")


def threshold_from_seed(seed: int) -> int:
    mod = seed % 3
    if mod == 0:
        return 15
    if mod == 1:
        return 12
    return 9


def api_spotcheck(seed: int) -> tuple[str, str, str]:
    """
    Returns: (term, songs_returned_str, api_status)
    api_status in {OK, FAILED, INVALID_RESPONSE}
    songs_returned_str is a number as string or 'N/A'
    """
    term = "weezer" if (seed % 2 == 0) else "drake"
    url = "https://itunes.apple.com/search"
    params = {"entity": "song", "limit": 5, "term": term}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        return term, "N/A", "FAILED"

    try:
        data = resp.json()
        if not isinstance(data, dict):
            return term, "N/A", "INVALID_RESPONSE"
        results = data.get("results")
        if not isinstance(results, list):
            return term, "N/A", "INVALID_RESPONSE"

        count_songs = 0
        for item in results:
            if isinstance(item, dict) and item.get("kind") == "song":
                count_songs += 1

        return term, str(count_songs), "OK"
    except (ValueError, TypeError):
        # ValueError can occur if JSON decoding fails; TypeError for unexpected shapes
        return term, "N/A", "INVALID_RESPONSE"


def main() -> None:
    student_key = input("Student key: ")
    seed = compute_seed(student_key)

    threshold = threshold_from_seed(seed)

    total_skus = 0
    reorder_count = 0

    while True:
        sku = prompt_nonempty_sku()
        if sku == "DONE":
            break

        on_hand = prompt_on_hand()
        total_skus += 1

        if on_hand < threshold:
            reorder_count += 1

    term, songs_returned, api_status = api_spotcheck(seed)

    # Output (exact labels)
    print(f"Seed: {seed}")
    print(f"Threshold: {threshold}")
    print(f"SKUs entered: {total_skus}")
    print(f"Reorder flagged: {reorder_count}")
    print(f"Spotcheck term: {term}")
    print(f"Songs returned: {songs_returned}")
    print(f"API status: {api_status}")


if __name__ == "__main__":
    main()