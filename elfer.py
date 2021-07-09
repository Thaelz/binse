import lief
import sys
from IPython import embed


def get_vas_for_fos(filename, fos):
    elf = lief.parse(filename)
    vas = []
    for fo, _ in fos:
        foundVA = False
        for section in elf.sections:
            if section.file_offset < fo < \
                section.file_offset + section.size:
                offset = fo - section.file_offset
                vas += [section.virtual_address + offset]
                foundVA = True
                break

        if not foundVA:
            vas += [None]
    return vas



if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print_vas_for_fos(filename)