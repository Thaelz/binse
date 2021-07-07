from rich.text import Text
from rich.console import Console
from binascii import hexlify

def hexdump(buffer, offset, bytesperline=16):

    console = Console()
    for i in range(0, len(buffer), bytesperline) :
        data = buffer[i: i + bytesperline]
        line  = Text("{:08x}".format(offset + i))
        line += "    "
        line += ''.join([ char if not ind or ind % 2 else ' ' + char
                    for ind,char in enumerate(hexlify(data).decode())
                    ]
                  )
        line += "    "
        line += ''.join([ chr(c) if c >= 0x20 and c < 0x7f else '.' for c in data])
        line.stylize('medium_purple1', 0, 8)
        console.print(line)


if __name__ == '__main__':
    with open("random.bin", "rb") as fin:
        hexdump(fin.read()[160:160+48], 160)
