"""make.fun entry: The Postmortem That Made Us Laugh.

This script is the code entry for the make.fun bounty
"The Postmortem That Made Us Laugh"
(https://make.fun/bounty/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3).

It reads the one-line entry stored in ``line.txt`` next to this script,
validates that it is one or two sentences and at most 400 characters,
and writes its exact bytes to the output path
(``/output/entry.txt`` by default, or ``MAKEFUN_OUTPUT`` when set).

No network access. Deterministic: the same input always produces the
same output bytes.
"""

import hashlib
import os
import re
import sys
from pathlib import Path

MAX_CHARS = 400
DEFAULT_OUTPUT = "/output/entry.txt"
# A sentence ends at terminal punctuation followed by a capital letter
# or the end of the text. This keeps abbreviations such as "p.m."
# (whose periods are followed by lowercase letters) from being
# counted as sentence ends.
SENTENCE_END_RE = re.compile(r"[.!?]+(?=\s*(?:[A-Z]|\Z))")


def count_sentences(text):
    """Count sentences by groups of sentence-ending punctuation."""
    return len(SENTENCE_END_RE.findall(text))


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    source = Path(__file__).resolve().parent / "line.txt"
    if not source.is_file():
        fail("line.txt not found: %s" % source)
    data = source.read_bytes()
    text = data.decode("utf-8")

    sentences = count_sentences(text)
    if sentences < 1 or sentences > 2:
        fail(
            "line.txt must contain exactly one or two sentences, "
            "found %d" % sentences
        )

    if len(text) > MAX_CHARS:
        fail(
            "line.txt must be at most %d characters, "
            "found %d" % (MAX_CHARS, len(text))
        )

    output_path = os.environ.get("MAKEFUN_OUTPUT") or DEFAULT_OUTPUT
    output = Path(output_path)
    if output.parent != Path(""):
        output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)

    written_hash = hashlib.sha256(output.read_bytes()).hexdigest()
    expected_hash = hashlib.sha256(data).hexdigest()
    if written_hash != expected_hash:
        fail(
            "output verification failed: SHA-256 mismatch "
            "(wrote %s, expected %s)" % (written_hash, expected_hash)
        )

    print("wrote %s (%d bytes, sha256 %s)" % (output, len(data), written_hash))


if __name__ == "__main__":
    main()
