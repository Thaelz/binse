from IPython import embed
import re
import logging
import sys
import lief
from rich.console import Console
from rich.text import Text
from hexdump import hexdump
from binascii import hexlify
from elfer import get_vas_for_fos

log = logging.getLogger("rich")

def print_hexdump(ba, start, end):
    """
    Wrap hexdump to print 16 bytes before our pattern
    and 16 bytes after.
    """
    wrap_range = (end - start) // 2
    if wrap_range < 16:
        wrap_range = 16
    wrap_start = (start & 0xfffffffffffffff0) - wrap_range
    wrap_end   = (end   & 0xfffffffffffffff0) + 2*wrap_range
    hexdump(ba[wrap_start:wrap_end], wrap_start, highlight_range=(start, end))

def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield (i, i+len(p))
        i = s.find(p, i+1)

def search_occurence(filename, ref, margin=16, verbose=False, isELF=False):
    """ search_occurence
    ref   : reference byte array to look for
    ba    : byte array to search inside for ref
    margin: nb of bytes to show before and after match
    """
    l = []
    with open(filename, "rb") as fin:
        ba = fin.read() 
    
    isELF = ba.startswith(b'\x7fELF')

    log.debug('{} ref: {} - ba {} (cropped)'.format('search_occurence', ref, ba[:16]))
    
    for start, end in findall(ref, ba):
        l += [(start, end)]

    if isELF:
        elf = lief.parse(filename)
        vas = get_vas_for_fos(elf, l)


    console = Console()
    if len(l) <= 0:
        text = Text("No match found", style="red")
        text.append(" for {}".format(hexlify(ref).decode()))
        console.print(text)
        return

    for i in range(len(l)):
        start, end = l[i]
        text = Text("#{:03} - offset 0x{:08x}".format(i+1, start))
        if isELF and not elf.is_pie:
            text.append(" - vaddr 0x{:08x}".format(vas[i]))
        text.stylize("bold magenta", 0, 5)
        text.stylize("blue", 14, 25)
        text.stylize("blue", 33, 43)
        console.print(text)

        print_hexdump(ba, start, end)
        
    
