"""The file loads a real ClarifyBench sample, builds one bag of possible values per book_flight detail, 
and computes each detail’s certainty (1, 1/n, or ε). 
Then it multiplies them to get SAGE’s score for the whole call, 
showing how unsure the robot is before asking anything."""

import json

AIRPORTS = ["ATV", "BOS", "CDG", "CIA", "CRH", "GFD", "HKG", "HND", "JFK", "LAX",
            "LHR", "MPC", "OKD", "ORD", "PEK", "PHV", "PVG", "RMS", "SBK", "SFO",
            "SHD", "SSV", "SVP", "WLB"]
CLASSES = ["economy", "business", "first"]
EPSILON = 0.0001   # certainty for an unknown value with no fixed list (like a date)

SAMPLE = "ClarifyBench/ClarifyBench/ClarifyBench_A/02956f7a.json"


def load_sample(path):
    """Read one ClarifyBench JSON file and return it as a dict."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def card_ids(sample):
    """The credit cards that exist in this sample's world."""
    return list(sample["initial_config"]["TravelAPI"]["credit_card_list"].keys())


def uniform_bag(domain):
    """Unknown detail with a fixed list: every value gets 1 / len(domain)."""
    return {v: 1 / len(domain) for v in domain}


def known_bag(value):
    """Known detail: one value with weight 1."""
    return {value: 1.0}


def certainty(bag):
    """Biggest weight in the bag. bag = None means unknown and unbounded."""
    if bag is None:
        return EPSILON
    return max(bag.values())


# ---------- test ----------
if __name__ == "__main__":
    sample = load_sample(SAMPLE)
    print("Cards in this world:", card_ids(sample))

    # Situation: the user said "Book a flight from ORD to LAX".
    # Class and date were not mentioned.
    bags = {
        "travel_from": known_bag("ORD"),
        "travel_to": known_bag("LAX"),
        "travel_class": uniform_bag(CLASSES),
        "travel_date": None,                      # unbounded and unknown
        "card_id": uniform_bag(card_ids(sample)),
    }

    total = 1.0
    for name, bag in bags.items():
        c = certainty(bag)
        print(f"{name}: certainty = {c:.4f}")
        total *= c
    print(f"Whole call certainty = {total:.6f}")