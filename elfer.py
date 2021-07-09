import sys
from IPython import embed


def get_vas_for_fos(elf, fos):
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
