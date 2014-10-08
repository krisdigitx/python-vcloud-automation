#!/usr/bin/python
__author__ = 'kshk'
import os
os.sys.path.append(os.path.dirname(os.path.abspath('.')))

from optparse import OptionParser
from vcore.vcloud import vcloud

def main():
    parser = OptionParser(usage='usage: %prog [options] configfile',version="%prog 2.5")
    parser.add_option('-c', '--config',
                      dest="config_file",
                      help='deploy a Vcloud VAPP or VM'
                        )
    options, remainder = parser.parse_args()
    print remainder
    if len(remainder) > 0:
        parser.error("wrong number of arguments")
    if not options.config_file:
        parser.error('vcloud config file not given')
    vcloud(options)

if __name__ == "__main__":
    main()

