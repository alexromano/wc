import sys
from typing import Optional
from typing_extensions import Annotated

import typer

from ccwc.counts import Counts


app = typer.Typer()

def get_file_byte_buffer(file_name: Optional[str]) -> Optional[bytes]:
    if file_name:
        try:
            return open(file_name, 'rb')
        except OSError:
            print("File does not exist")
    else:
        return sys.stdin.buffer

def calculate_counts(lines, words, count, characters, file_bytes: bytes) -> Counts:
    line_count, word_count, byte_count, char_count = 0, 0, 0, 0
    for line in file_bytes.readlines():
        if lines:
            line_count += 1
        elif words:
            word_count += len(line.split())
        elif count:
            byte_count += len(line)
        elif characters:
            char_count += len(line.decode())
        else:
            line_count += 1
            word_count += len(line.split())
            byte_count += len(line)
    return Counts(line_count=line_count, word_count=word_count, byte_count=byte_count, char_count=char_count)

def print_counts(file_name: Optional[str], count, lines, words, characters, counts: Counts):
    if lines:
        print(f"{counts.line_count} {file_name or ''}")
    elif words:
        print(f"{counts.word_count} {file_name or ''}")
    elif count:
        print(f"{counts.byte_count} {file_name or ''}")
    elif characters:
        print(f"{counts.char_count} {file_name or ''}")
    else:
        print(f"{counts.line_count} {counts.word_count} {counts.byte_count} {file_name or ''}")

@app.command()
def main(
    file_name: Annotated[Optional[str], typer.Argument()] = None,
    count: Annotated[bool, typer.Option('-c')] = False,
    lines: Annotated[bool, typer.Option('-l')] = False,
    words: Annotated[bool, typer.Option('-w')] = False,
    characters: Annotated[bool, typer.Option('-m')] = False,
    ):
    file_bytes = get_file_byte_buffer(file_name)

    counts = calculate_counts(lines, words, count, characters, file_bytes)

    print_counts(file_name, count, lines, words, characters, counts)

if __name__ == '__main__':
    app()