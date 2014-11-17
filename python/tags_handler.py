#! /usr/bin/env python

import sys
import os


#from subprocess import call
import subprocess
#from subprocess import Popen
from paths_resolver import PathsResolver

class TagsHandler:
    def __init__(self):
        if (sys != None):
            sys.path.append(os.getcwd())

    def generateTagsFile(self):
        if (self.which('ctags') != None):
            #NOTE wouldn't a Popen(['ctags','--version']) be more to the point?
            shellIndependantCommandArray = self.getCtagsCommand()
            self.executeCommandAsyncly(shellIndependantCommandArray)
        else:
            print 'ctags executable not found. To use this command, please install it.'
        #TODO: Into help. If ctags doesn't create a file, make sure it is exurbitant-ctags
        # To check the version type 'man ctags' and at the top it should say Exurbitant Ctags (on *nix)


    def getCtagsCommand(self):
        finalCommandArray = []

        # NOTE that the \1 needed double escaping
        ctagsShellCommand = ['ctags','--recurse','--fields=+l','--langdef=XML','--langmap=Java:.java,XML:.xml','--languages=Java,XML','--regex-XML=/id="([a-zA-Z0-9_]+)"/\\1/d,definition/']
        finalCommandArray += ctagsShellCommand

        ctagsTargetFile = '.tags' #TODO make tag file name/location dynamic
        finalCommandArray += ['-f', ctagsTargetFile]

        sourcePaths = PathsResolver().getAllSourcePaths();
        finalCommandArray += sourcePaths

        #print " ".join(finalCommandArray)
        return finalCommandArray


    def executeCommandAsyncly(self, commandArray):
        print " ".join(commandArray)

        # TODO This is qite messy. Clean it up

        if not os.path.isfile('.tags'):
            # No tags file? CREATE IT!
            print 'creating new tags file'
            subprocess.Popen(commandArray)
        else:
            # There is a tags file? Um... Let's see if it's valid first...
            if self.isValidTagsFile():
                # Check, go on adding stuff
                print 'appending to tags file'
                commandArray.insert(3, '-a')
                subprocess.Popen(commandArray)
            else:
                # INVALID. Delete the file and start over. 
                # this can happen when you've tryed regenerating tags before the last ctags task had finished
                os.remove('.tags')
                print 'creating new tags file'
                subprocess.Popen(commandArray)



    def isValidTagsFile(self):
        with open('.tags', 'U') as f:
            lines = f.readlines(6)

            if (lines[0].startswith('!_TAG_FILE_FORMAT')
                and lines[1].startswith('!_TAG_FILE_SORTED')
                and lines[2].startswith('!_TAG_PROGRAM_AUTHOR')
                and lines[3].startswith('!_TAG_PROGRAM_NAME')
                and lines[4].startswith('!_TAG_PROGRAM_URL')
                and lines[5].startswith('!_TAG_PROGRAM_VERSION')):
                return True
            else:
                return False


    def which(self, program):
        # method copied from http://stackoverflow.com/a/377028
        import os
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None


