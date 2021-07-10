# binse

A simple and colorful binary searching tool printing the hexdump surrounding each match. Some features are available:
- Process multiple files if provided
- Show ELF virtual addresses (if not PIC executable)
- Highlight matching hex
- Disable hexdump


## Install

To install simply use pip (with setuptools):
```
$ git clone https://github.com/Thaelz/binse .
$ cd binse
$ pip install .
```

And then, you should be able to execute:
```
$ binse -h
```


## Use

To seek all 'ls' in /bin/ls
```
$ binse 6c73 /bin/ls
```

But since we're searching ASCII, let's provide it as a string
```
$ binse ls /bin/ls
```

What about multiple files at the same time?
```
$ binse 7ffe /bin/ls /bin/wc
```

Disable hexdump, nothing more `--simple`
```
$ binse 4142 -s /bin/ls
```


## Improvements

See `TODO.md` or file an issue!
Make a license? ..



