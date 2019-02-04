'''
Description:
Rename and number selected items.

Installation:
Place this file in the `lxserv` directory inside your user scripts directory.
'''

import lx
import lxu
import lxu.select

class Renumber(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        '''
        The initial launching of Modo will perform a shallow execution before the
        scene state is established. Use try/except to prevent console error.
        '''
        try:
            self.selection = lxu.select.ItemSelection().current()
        except:
            self.selection = []

        self.dyna_Add('Base Name', lx.symbol.sTYPE_STRING)
        self.dyna_Add('Start Name', lx.symbol.sTYPE_STRING)
        self.dyna_Add('End Name', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def basic_Execute(self, msg, flags):
        baseName = self.cleanString(self.dyna_String(0))
        startName = self.cleanString(self.dyna_String(1))
        endName = self.cleanString(self.dyna_String(2))

        if baseName:
            for i, item in enumerate(self.selection, start=1):
                if startName and i == 1:
                    item.SetName(baseName + startName)
                elif endName and i == len(self.selection):
                    item.SetName(baseName + endName)
                elif startName:
                    item.SetName(baseName + str(i - 1))
                else:
                    item.SetName(baseName + str(i))
        else:
            lx.out('Base name invalid')

    def cmd_Query(self, index, vaQuery):
        """
        Put the name of the first selected item in the dialog's name field.
        """
        ValueArray = lx.object.ValueArray()
        ValueArray.set(vaQuery)
        ValueArray.AddString(self.selection[0].UniqueName())
        return lx.result.OK

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        # Prevent bogus stack trace errors.
        pass

    def cleanString(self, val=None):
        if not val:
            return

        illegalChars = ['^', '<', '>', '/', '\\', '{', '}', '[', ']',
                        '~', '`', '$', '.', '?', '%', '&', '@', '*',
                        '(', ')', '!', '+', '#', '\'', '\"']

        for char in illegalChars:
            val = val.replace(char, '')

        return val

lx.bless(Renumber, 'bird.renumber')
