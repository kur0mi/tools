##################################################
#### ***  help you to create a makefile!  *** ####

#
# author: kur0mi
# email:  <1601631551@qq.com>
# date:   2017/11/18
#

# description:
#
# ** for use it, you may need a c/c++ compiler and python runtime.

# usage:
#
# **  first copy this script to your directory,
# **  second type 'python make.py' to create a makefile,
# **  then type 'make' to execute it!

###################################################


####################################################
# Custom part: modify it by yourself
#

# header file(.h) path
SRCDIRS = ["src"]
LIBDIRS = []

# which ones you wanna to compile
SRC_CXX = ["design/4.cpp"]

# C++ compile and link option
CXX = "g++"
FLAGS = "-g -O2 -Wall -std=c++1z"

#
#
###############################################################


###############################################################
# Stable part: please do not modify the code below
#

FILENAME = "Makefile"

HEAD = " ".join(['-I' + x for x in SRCDIRS] + ['-L' + x for x in LIBDIRS])
LINK = ""
DEP = "-MM"

COMPILE = CXX + ' ' + FLAGS + ' ' + HEAD
LINK = CXX + ' ' + FLAGS + ' ' + LINK
DEP = CXX + ' ' + DEP + ' ' + HEAD

#
#
###############################################################


import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

linkfile = []
allbase = []

def getHead():
    # make the total target
    return 'all: ' + ' '.join([x.replace('.cpp', '.exe')
                               for x in SRC_CXX]) + '\n'


def getPart(cpp):
    r = ''
    s0 = os.popen("{} {}".format(DEP, cpp)
                  ).readline().strip()
    s1 = "\n\t" + "{} -c $< -o $@".format(COMPILE) + "\n"

    base = s0.split('.')[0]
    if base not in allbase:
        r += s0 + s1
        allbase.append(base)
    linkfile.append(base + '.o')
    h = filter(lambda x: base not in x, s0.split(' '))
    cpps = [x.replace('.h', '.cpp') for x in h]
    for cpp in cpps:
        r += getPart(cpp)

    return r


def getLink(cpp):
    exe = cpp.replace('.cpp', '.exe')
    r = ''
    r += exe + ': ' + ' '.join(linkfile)
    r += '\n\t' + LINK + '$^ -o $@' + '\n'
    return r


def getCoffee():
    r = ''
    r += '.PHONY: clean' + '\n'
    r += 'clean: ' + '\n'
    r += '\t' + 'powershell -c "rm ' + '*.o"' + '\n'
    return r


def main():
    with open(FILENAME, "w") as fp:
        r = ''
        r += getHead()
        global linkfile
        for x in SRC_CXX:
            r += getPart(x)
            r += getLink(x)
            linkfile = []
        r += getCoffee()
        fp.write(r)


if __name__ == '__main__':
    main()
