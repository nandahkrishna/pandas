#!/usr/bin/env python

import math
import os
import sys
import xml.etree.ElementTree as et


def parse_results(filename):
    tree = et.parse(filename)
    root = tree.getroot()
    skipped = []

    current_class = ""
    i = 1
    assert i - 1 == len(skipped)
    for el in root.findall("testcase"):
        cn = el.attrib["classname"]
        for sk in el.findall("skipped"):
            old_class = current_class
            current_class = cn
            name = "{classname}.{name}".format(
                classname=current_class, name=el.attrib["name"]
            )
            msg = sk.attrib["message"]
            out = ""
            if old_class != current_class:
                ndigits = int(math.log(i, 10) + 1)

                # 4 for : + space + # + space
                out += "-" * (len(name + msg) + 4 + ndigits) + "\n"
            out += "#{i} {name}: {msg}".format(i=i, name=name, msg=msg)
            skipped.append(out)
            i += 1
            assert i - 1 == len(skipped)
    assert i - 1 == len(skipped)
    # assert len(skipped) == int(root.attrib['skip'])
    return "\n".join(skipped)


def main():
    test_files = ["test-data-single.xml", "test-data-multiple.xml", "test-data.xml"]

    print("SKIPPED TESTS:")
    for fn in test_files:
        if os.path.isfile(fn):
            print(parse_results(fn))
    return 0


if __name__ == "__main__":
    sys.exit(main())
