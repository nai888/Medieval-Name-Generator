import random
import argparse
import sys
import csv

from given_male import given_male
from given_female import given_female
from surnames_noble import noble_surnames
from surnames_commoner import commoner_surnames


def build_pools(gender, social_class):
    # First names
    if gender == "male":
        first_pool = given_male
    elif gender == "female":
        first_pool = given_female
    else:
        first_pool = given_male + given_female

    # Surnames
    if social_class == "noble":
        last_pool = noble_surnames
    elif social_class == "commoner":
        last_pool = commoner_surnames
    else:
        last_pool = noble_surnames + commoner_surnames

    return first_pool, last_pool


def generate_names(
    count,
    gender=None,
    social_class=None,
    unique_last=False,
    unique_full=False,
    seed=None,
):
    if seed is not None:
        random.seed(seed)

    first_pool, last_pool = build_pools(gender, social_class)

    if unique_last and count > len(last_pool):
        raise ValueError(
            f"Requested {count} names with unique last names, "
            f"but only {len(last_pool)} surnames in the selected pool."
        )

    if unique_full:
        total_combos = len(first_pool) * len(last_pool)
        if count > total_combos:
            raise ValueError(
                f"Requested {count} unique full names, "
                f"but only {total_combos} unique combos possible "
                f"({len(first_pool)} firsts × {len(last_pool)} lasts)."
            )

    results = []

    if unique_last:
        # Sample surnames without replacement; pair with random firsts
        for ln in random.sample(last_pool, count):
            fn = random.choice(first_pool)
            results.append((fn, ln))
        # If also unique_full (belt-and-suspenders), ensure no duplicates
        if unique_full:
            seen = set()
            fixed = []
            for fn, ln in results:
                pair = (fn, ln)
                if pair in seen:
                    # pick a new first that doesn't collide with same last
                    candidates = [f for f in first_pool if (f, ln) not in seen]
                    if not candidates:
                        raise ValueError(
                            "Ran out of unique first names for a chosen last."
                        )
                    fn = random.choice(candidates)
                    pair = (fn, ln)
                seen.add(pair)
                fixed.append(pair)
            results = fixed
        return results

    # Free pairing; enforce unique_full if requested
    if not unique_full:
        for _ in range(count):
            results.append((random.choice(first_pool), random.choice(last_pool)))
        return results

    used = set()
    attempts = 0
    max_attempts = count * 20
    while len(results) < count and attempts < max_attempts:
        pair = (random.choice(first_pool), random.choice(last_pool))
        if pair not in used:
            used.add(pair)
            results.append(pair)
        attempts += 1
    if len(results) < count:
        # Systematic fill (very unlikely to be needed)
        for fn in first_pool:
            for ln in last_pool:
                pair = (fn, ln)
                if pair not in used:
                    results.append(pair)
                    used.add(pair)
                    if len(results) == count:
                        break
            if len(results) == count:
                break
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate Old/Middle English character names."
    )
    parser.add_argument(
        "count",
        type=int,
        nargs="?",
        default=5,
        help="Number of names to generate (default: 5)",
    )
    parser.add_argument("--male", action="store_true", help="Use male given names only")
    parser.add_argument(
        "--female", action="store_true", help="Use female given names only"
    )
    parser.add_argument("--noble", action="store_true", help="Use noble surnames only")
    parser.add_argument(
        "--commoner", action="store_true", help="Use commoner surnames only"
    )

    # Uniqueness & reproducibility
    parser.add_argument(
        "--unique-last", action="store_true", help="No surname repeats in the batch"
    )
    parser.add_argument(
        "--unique-full",
        action="store_true",
        help="No exact full name repeats in the batch",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducible output"
    )

    # Output options
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Write newline-separated full names to this text file",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Write first/last columns to this CSV file",
    )
    parser.add_argument(
        "--no-stdout",
        action="store_true",
        help="Do not print names to stdout (only write files)",
    )

    args = parser.parse_args()

    # Filters
    gender = "male" if args.male else "female" if args.female else None
    social_class = "noble" if args.noble else "commoner" if args.commoner else None

    try:
        pairs = generate_names(
            args.count,
            gender=gender,
            social_class=social_class,
            unique_last=args.unique_last,
            unique_full=args.unique_full,
            seed=args.seed,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Write files if requested
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for fn, ln in pairs:
                f.write(f"{fn} {ln}\n")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["first", "last"])
            for fn, ln in pairs:
                writer.writerow([fn, ln])

    # Print to stdout unless suppressed
    if not args.no_stdout:
        for fn, ln in pairs:
            print(f"{fn} {ln}")


if __name__ == "__main__":
    main()
