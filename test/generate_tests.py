#!/usr/bin/env python

# This will generate a test suite.
# Based on code from python-sha3.

def generate():
    FILES = [
        ('test/data/ShortMsgKAT_224.txt', 224),
        ('test/data/ShortMsgKAT_256.txt', 256),
        ('test/data/ShortMsgKAT_384.txt', 384),
        ('test/data/ShortMsgKAT_512.txt', 512),
        ('test/data/LongMsgKAT_224.txt', 224),
        ]

    print """
// This file generated by generate_tests.py

var sys = require('sys');
var assert = require('assert');
var SHA3 = require('./../build/Release/sha3');

"""

    for path, hashlen in FILES:
        contents = file(path).read().split('Len = ')
        for test in contents:
            lines = test.split('\n')
            if lines and len(lines) and not lines[0].startswith('#'):
                length = int(lines[0])
                if length % 8 == 0 and length != 0:
                    msg = lines[1].split(' = ')[-1].lower()
                    md = lines[2].split(' = ')[-1].lower()
                    name = path.split('/')[-1].split('.')[0]

                    print """// %s %s
        inst = new SHA3.SHA3Hash(%s);
        inst.update(new Buffer(%r, 'hex'));
        assert.equal(inst.digest('hex'), %r);
        sys.print(".");

""" % (name, length, hashlen, msg, md)
    
    print 'sys.print("\\n");'

if __name__ == '__main__':
    generate()
