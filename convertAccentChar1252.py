#!/usr/bin/python
# -*- coding: cp1252 -*-

import sys
from GlyphSprites import Sprites

def enc(letter):
    return letter.encode('utf-8').decode('cp1252')

dictGlyph = {
    '�' : ('e',Sprites.letterEacute),
    '�' : ('e',Sprites.letterEgrave),
    '�' : ('e',Sprites.letterEcirc),
    '�' : ('e',Sprites.letterEuml),
    '�' : ('E',None),
    '�' : ('E',None),
    '�' : ('E',None),
    '�' : ('E',None),
    '�' : ('a',Sprites.letterAgrave),
    '�' : ('A',None),
    '�' : ('u',Sprites.letterUgrave),
    '�' : ('o',Sprites.letterOcirc),
    '�' : ('O', None)
}

maxCustomChar = 8

def convertMsg(message):
    return convertMsgParam(message, [], [], maxCustomChar)

def convertMsgParam(message,glyphList,charList,maxChar):
    """ return message and glyph list """
    newMsg = ''
    offsetGlyphList = len(glyphList) - len(charList) 

    for c in message:
        if c in dictGlyph:
            if c in charList: #glyph has already been added to the list, so use it!
                newMsg += chr(offsetGlyphList + charList.index(c))
            else:
                glyphTuple = dictGlyph[c]
                if len(glyphList) < maxChar and glyphTuple[1] != None: # is there still a free place? is a glyph defined ?
                    glyphList.append(glyphTuple[1])
                    charList.append(c)
                    newMsg += chr(len(glyphList)-1)
                else:
                    newMsg += glyphTuple[0] #use replacement char (because there is no glyph or because there is no more place for custom char) 
        else:
            newMsg += c #add normal char to the message
    return (newMsg,glyphList,charList)

if __name__ == '__main__':
    print(repr(dictGlyph))
    if len(sys.argv) > 1:
        print(repr(convertMsg(" ".join(sys.argv[1:]).decode('utf-8').encode('cp1252'))))
    else:
        print(repr(convertMsg('Accents du a : �\nAccents du e: �������\nAccents du u: �\nAccents du o : ��')))

