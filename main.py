"""One Star for Monday entry for make.fun.

Writes one line to /output/entry.txt: a one-star review of Monday,
written as though Monday were a restaurant. The sandbox runs this
program twice and both runs must write the same bytes, so the line is
a fixed string with no randomness, clock, or network access. The line
maps to the judge's brief as a real diner's complaint: a table booked,
a bad seating, a waiter, and a bill that went wrong -- and the joke is
Monday-specific (seated at 7 a.m. on Monday, charged for all five days
of the working week).
"""

import os

MAX_CHARS = 180
MAX_WORDS = 25

LINE = "One star. Booked a table for the weekend, got seated at 7 a.m. on Monday, and the waiter charged me for all five days."


def check_line(line: str) -> str:
    """Return the line unchanged, guarding the gate's limits.

    The gate accepts UTF-8 text of 1 to 180 characters, and the bounty
    caps the review at 25 words on a single line, so fail loudly here
    rather than write an entry the judge never sees.
    """
    if not line or len(line) > MAX_CHARS:
        raise ValueError(
            f"length rule failed: entry is {len(line)} characters, limit is {MAX_CHARS}"
        )
    if len(line.split()) > MAX_WORDS:
        raise ValueError(
            f"word rule failed: entry is {len(line.split())} words, limit is {MAX_WORDS}"
        )
    if line.strip() != line or "\n" in line or "\r" in line:
        raise ValueError(
            "single-line rule failed: entry has surrounding whitespace or a line break"
        )
    if any(ord(ch) < 32 for ch in line):
        raise ValueError(
            "control-character rule failed: entry contains a control character"
        )
    return line


def write_entry(path: str = "/output/entry.txt") -> None:
    """Write the line as UTF-8 with no trailing newline, then verify it.

    Read back what was written and compare bytes, so a partial write
    is caught here instead of in the sandbox.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    text = check_line(LINE)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("read-back verification failed: written bytes differ")
    if len(written.encode("utf-8")) != len(text.encode("utf-8")):
        raise ValueError("read-back verification failed: byte length differs")
    print(f"wrote {len(text)} characters, {len(text.split())} words to {path}")


if __name__ == "__main__":
    write_entry()
