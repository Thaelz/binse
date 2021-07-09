from rich.text import Text
from rich.console import Console
from binascii import hexlify

def highlight_bytes(ba : Text, offset : int, 
                    start : int, end : int,
                    bytesperline: int):
    endline = offset + bytesperline
    if offset <= start <= endline:
        h_start = (start - offset)*3
    elif start <= offset < end:
        h_start = 0
    else:
        h_start = None

    if offset < end <= endline:
        h_end = (end - offset)*3
    else:
        h_end = len(ba)


    if h_start is not None:
        ba.stylize('red', h_start, h_end)

    return ba



def hexdump(buffer, offset, bytesperline=16,
    highlight_range=None, bytes_addr=4):
    """
    hexdump print the *buffer* as it is starting at *offset*
    with *bytesperline* bytes per .. line!
    """
    console = Console()
    for i in range(0, len(buffer), bytesperline) :
        data = buffer[i: i + bytesperline]
        addr = "{:x}".format(offset + i)
        line  = Text("{}".format(addr.rjust(bytes_addr<<1, '0')))
        line += "    "
        bytes = Text(''.join([ char if not ind or ind % 2 else ' ' + char
                    for ind,char in enumerate(hexlify(data).decode())
                    ]
                  ))
        if highlight_range is not None:
            h_start, h_end = highlight_range
            bytes = highlight_bytes(bytes, offset + i, h_start, h_end, bytesperline)
        line += bytes
        line += "    "
        line += ''.join([ chr(c) if c >= 0x20 and c < 0x7f else '.' for c in data])
        line.stylize('medium_purple1', 0, (bytes_addr<<1) + 1)
        console.print(line)


if __name__ == '__main__':
    with open("random.bin", "rb") as fin:
        hexdump(fin.read()[160:160+48], 160)
