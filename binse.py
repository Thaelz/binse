#!/usr/bin/env python3
import sys
import argparse
import logging
from rich.logging import RichHandler
from rich.text import Text
from rich.console import Console
from binascii import unhexlify

from searcher import search_occurence

def cmdline_args():
        # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("pattern",
                   help="Pattern to search for, hexstring by default")
    p.add_argument("file", nargs='+',
                   help="File to look inside")
    p.add_argument("--str", action="store_true",
                   help="pattern is defined as a string")
    p.add_argument("-v", "--verbosity", action="store_true", 
                   help="increase output verbosity (default: false)")
                   
    #group1 = p.add_mutually_exclusive_group(required=True)
    #group1.add_argument('--enable',action="store_true")
    #group1.add_argument('--disable',action="store_false")

    return(p.parse_args())


if __name__ == '__main__':
    
    if sys.version_info<(3,5,0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)

    # Setup logging
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    log = logging.getLogger("rich")
    console = Console()
        
    args = None
    pattern = None
    try:
        args = cmdline_args()
        log.debug(args)

    except:
        log.error('usage: {} PATTERN FILE'.format(sys.argv[0]))
        sys.exit(1)

    logging_level = "DEBUG" if args.verbosity else "INFO"
    log.setLevel(logging_level)

    if args.str:
        pattern = args.pattern.encode('unicode_escape')
    else:
        pattern = unhexlify(args.pattern.encode('unicode_escape'))

    logging.debug("Pattern : {}".format(pattern))
    for f in args.file:
        if len(args.file) > 1:
            pf = Text("Processing {}..".format(f))
            pf.stylize("green", 11, 11+len(f))
            console.print(pf)
        search_occurence(f, pattern)

    