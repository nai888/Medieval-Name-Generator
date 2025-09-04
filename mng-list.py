import argparse
import sys

from given_male import given_male
from given_female import given_female
from surnames_noble import noble_surnames
from surnames_commoner import commoner_surnames


def list(list):
    if list == "ffirst":
        return given_female
    elif list == "mfirst":
        return given_male
    elif list == "clast":
        return commoner_surnames
    elif list == "nlast":
        return noble_surnames


def main():
    parser = argparse.ArgumentParser(
        description="Generate Old/Middle English character names."
    )

    parser.add_argument(
        "--list",
        type=str,
        default=None,
        help="Which list to write out. Valid values are ffirst, mfirst, clast, and nlast.",
    )

    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Write space-separated names to this text file",
    )

    args = parser.parse_args()

    names = list(args.list)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for name in names:
                f.write(f"{name} ")


if __name__ == "__main__":
    main()
