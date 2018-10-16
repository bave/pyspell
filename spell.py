#!/usr/bin/env python

import re
import json
import pickle

class lcsobj():

    def __init__(self, seq, lineid, refmt):
        self._refmt = refmt
        if isinstance('string', type(seq)) == True:
            self._lcsseq = re.split(self._refmt, seq.lstrip().rstrip())
        else:
            self._lcsseq = seq
        self._lineids = [lineid]
        self._pos = []
        return

    def getlcs(self, seq):
        if isinstance('string', type(seq)) == True:
            seq = re.split(self._refmt, seq.lstrip().rstrip())
        count = 0
        lastmatch = -1
        for i in range(len(self._lcsseq)):
            #if self._lcsseq[i] == '*':
            if self._ispos(i) == True:
                continue
            for j in range(lastmatch+1, len(seq)):
                if self._lcsseq[i] == seq[j]:
                    lastmatch = j
                    count += 1
                    break
        return count

    def insert(self, seq, lineid):
        if isinstance('string', type(seq)) == True:
            seq = re.split(self._refmt, seq.lstrip().rstrip())
        self._lineids.append(lineid)
        pos = []
        temp = ""
        lastmatch = -1
        placeholder = False

        for i in range(len(self._lcsseq)):
            #if self._lcsseq[i] == '*':
            if self._ispos(i) == True:
                if not placeholder:
                    temp = temp + "* "
                placeholder = True
                continue
            for j in range(lastmatch+1, len(seq)):
                if self._lcsseq[i] == seq[j]:
                    placeholder = False
                    temp = temp + self._lcsseq[i] + " "
                    lastmatch = j
                    break
                elif not placeholder:
                    temp = temp + "* "
                    placeholder = True
        temp = temp.lstrip().rstrip()
        self._lcsseq = re.split(self._refmt, temp)

        for i in range(len(self._lcsseq)):
            if self._lcsseq[i] == '*':
                pos.append(i)
        self._pos = pos

    def tojson(self):
        temp = ""
        for i in self._lcsseq:
            temp = temp + i + " "
        ret = {}
        ret["lcsseq"] = temp
        ret["lineids"] = self._lineids
        ret["postion"] = self._pos
        return json.dumps(ret)

    def length(self):
        return len(self._lcsseq)

    def _ispos(self, idx):
        has = [i for i, x in enumerate(self._pos) if x == idx]
        if len(has) == 0:
            return False
        else:
            return True




class lcsmap():

    def __init__(self, refmt):
        self._refmt = refmt
        self._lcsobjs = []
        self._lineid = 0
        return

    def insert(self, entry):
        seq = re.split(self._refmt, entry.lstrip().rstrip())
        obj = self.match(seq)
        if obj == None:
            self._lineid += 1
            obj = lcsobj(seq, self._lineid, self._refmt)
            self._lcsobjs.append(obj)
        else:
            self._lineid += 1
            obj.insert(seq, self._lineid)

        param = []
        for i in obj._pos:
            param.append(seq[i])

        return obj, param

    def match(self, seq):
        if isinstance('string', type(seq)) == True:
            seq = re.split(self._refmt, entry.lstrip().rstrip())
        bestmatch = None
        bestmatch_len = 0
        seqlen = len(seq)
        for obj in self._lcsobjs:
            objlen = obj.length()
            if objlen < seqlen/2 or objlen > seqlen*2: continue

            l = obj.getlcs(seq)
            if l >= seqlen/2 and l > bestmatch_len:
                bestmatch = obj
                bestmatch_len = l
        return bestmatch

    def objat(self, idx):
        return self._lcsobjs[idx]

    def size(self):
        return len(self._lcsobjs)

    def dump(self):
        for i in self._lcsobjs:
            print(i.tojson())


def save(filename, spell_lcsmap):
    if type(spell_lcsmap) == lcsmap:
        with open(filename,'wb') as f:
            pickle.dump(spell_lcsmap, f)
    else:
        if __debug__ == True:
            print("%s isnt slm object"%filename)

def load(filename):
    with open(filename,'rb') as f:
        slm = pickle.load(f)
        if type(slm) == lcsmap:
            return slm
        else:
            if __debug__ == True:
                print("%s isnt slm object"%filename)
            return None
