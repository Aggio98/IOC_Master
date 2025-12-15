import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Simple CLI log processor"
    )

    parser.add_argument(
        "logfile",
        help="Path to the log file"
    )

    parser.add_argument(
        "--lines",
        type=int,
        default=10,
        help="Number of lines to read (default: 10)"
    )

    args = parser.parse_args()

    print(f"Log file: {args.logfile}")
    print(f"Lines: {args.lines}")

    try:
        with open(args.logfile, "r") as file:
            for i, line in enumerate(file):
                if i >= args.lines:
                    break
                print(line.strip())
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()