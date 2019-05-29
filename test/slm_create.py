#!/usr/bin/env python

import sys
sys.path.append("../")

import spell as s


if __name__ == '__main__':
    slm = s.lcsmap('[\\s]+')
    for i in sys.stdin.readlines():
        sub = i.strip('\n')
        obj = slm.insert(sub)
        #print(obj.get_id(), obj.param(sub))
    s.save('slm.pickle', slm)

slm.dump()
