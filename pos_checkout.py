# pos_checkout.py
# DATA 4000 — Assignment 5 (Exercise 1)

def compute_seed(student_key: str) -> int:
    return sum(ord(ch) for ch in student_key.strip())


def prompt_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Invalid input. Please try again.")
            continue
        return value


def prompt_positive_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Invalid input. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please try again.")


def prompt_int_min(prompt: str, minimum: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value < minimum:
                print("Invalid input. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please try again.")


def main() -> None:
    student_key = input("Student key: ")
    seed = compute_seed(student_key)

    subtotal = 0.0
    total_units = 0

    while True:
        item_name = input("Item name: ").strip()
        if item_name.upper() == "DONE":
            break
        if item_name == "":
            print("Invalid input. Please try again.")
            continue

        unit_price = prompt_positive_float("Unit price: ")
        quantity = prompt_int_min("Quantity: ", 1)

        subtotal += unit_price * quantity
        total_units += quantity

    # Discount logic
    discount_percent = 10 if (total_units >= 10 or subtotal >= 100) else 0
    discounted_total = subtotal * (1 - discount_percent / 100)

    # Seed-based perk
    perk_applied = "YES" if (seed % 2 == 1) else "NO"
    total = discounted_total
    if seed % 2 == 1:
        total -= 3.00

    if total < 0:
        total = 0.0

    # Output (exact labels)
    print(f"Seed: {seed}")
    print(f"Units: {total_units}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: {discount_percent}%")
    print(f"Perk applied: {perk_applied}")
    print(f"Total: ${total:.2f}")


if __name__ == "__main__":
    main()