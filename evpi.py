"""Level 2: EVPI. For each parameter, how much would the score improve
if the user answered it? The robot asks about the biggest one."""

from world import load_sample, card_ids, uniform_bag, known_bag, certainty, CLASSES, SAMPLE


def score(bags):
    """Whole call certainty = product of all certainties (same as Level 1's loop)."""
    total = 1.0
    for bag in bags.values():
        total *= certainty(bag)
    return total


def evpi(bags, param):
    """How much the score improves if `param` becomes certain."""
    after = dict(bags)               # a copy, so we don't change the real bags
    after[param] = {"answer": 1.0}   # imagine: this parameter is now known
    return score(after) - score(bags)


def best_question(bags):
    """EVPI for every parameter, and the one with the biggest EVPI."""
    values = {p: evpi(bags, p) for p in bags}
    best = max(values, key=values.get)
    return best, values


# ---------- test ----------
if __name__ == "__main__":
    sample = load_sample(SAMPLE)
    bags = {
        "travel_from": known_bag("ORD"),
        "travel_to": known_bag("LAX"),
        "travel_class": uniform_bag(CLASSES),
        "travel_date": None,
        "card_id": uniform_bag(card_ids(sample)),
    }

    # Turn 1
    print(f"Score now = {score(bags):.7f}")
    best, values = best_question(bags)
    for p, v in values.items():
        print(f"EVPI({p}) = {v:.7f}")
    print("Best question:", best)

    # The user answers the date
    bags["travel_date"] = known_bag("2024-08-10")

    # Turn 2
    print(f"\nAfter the date answer, score = {score(bags):.4f}")
    best, values = best_question(bags)
    for p, v in values.items():
        print(f"EVPI({p}) = {v:.4f}")
    print("Best question:", best)