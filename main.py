"""Sorry, I Heard That Wrong — make.fun entry (program/v1).

Writes one apology line (130 characters, UTF-8, no trailing newline) to
/output/entry.txt.

The speaker misheard "lock the front door" as "block the front door"
and, being a helpful device, carried the order out at once: it
barricaded the door with the sofa — then reports the result with
the flat pride of a gadget that has no idea it did anything wrong.
The laugh is the collision of a plausible mishearing with an
irreversible, over-literal act, undercut by the speaker congratulating
itself. No song title, no misheard name: a fresh mishearing, in the
device's own voice.

Standard library only. No network, no local imports, no writes
outside the output path the harness provides. Deterministic: the
same bytes on every run.
"""

import os
import sys

ENTRY = (
    "Sorry, I heard 'lock the front door' as 'block the front door' "
    "\u2014 I have barricaded it with the sofa and I am very proud "
    "of myself."
)


def main():
    line = ENTRY
    if not line or not line.strip():
        sys.exit("entry line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("entry line must be a single line")
    if not 1 <= len(line) <= 140:
        sys.exit("entry line must be 1-140 characters, got %d" % len(line))
    if line != line.strip():
        sys.exit("entry line must not start or end with whitespace")
    if "  " in line:
        sys.exit("entry line must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry line must not contain control characters")
    if not line.startswith("Sorry, I heard 'lock the front door'"):
        # The apology is the entry itself: it must never silently
        # go missing from the line.
        sys.exit("entry line must start with the Sorry apology")
    if "barricaded it with the sofa" not in line:
        # The barricade punchline is what makes the mishearing
        # land instead of staying a plain apology.
        sys.exit("entry line must keep the barricade punchline")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and verify the file is exactly the gated line, no newline.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("entry.txt does not match the gated line")
    print("wrote %s (%d chars, %d bytes)" % (path, len(line), len(data)))


if __name__ == "__main__":
    main()
