from IPython import embed
import re
import logging
import sys
from rich.console import Console
from rich.text import Text
from hexdump import hexdump

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
    hexdump(ba[wrap_start:wrap_end], wrap_start)

def search_occurence(ref, ba, margin=16, verbose=False):
    """ search_occurence
    ref   : reference byte array to look for
    ba    : byte array to search inside for ref
    margin: nb of bytes to show before and after match
    """
    l = []

    log.debug('{} ref: {} - ba {} (cropped)'.format('search_occurence', ref, ba[:16]))
    p = re.compile(ref)
    for e in p.finditer(ba):
        l += [(e.start(), e.end())]

    console = Console()
    if len(l) <= 0:
        text = Text("No match found", style="red")
        text.append(" for {}".format(ref.decode()))
        console.print(text)
        return

    for i in range(len(l)):
        start, end = l[i]
        text = Text("#{:03} - offset 0x{:08x}".format(i+1, start))
        text.stylize("bold magenta", 0, 5)
        text.stylize("blue", 14, 25)
        console.print(text)

        print_hexdump(ba, start, end)
        
    
