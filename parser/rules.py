#>>> class test:
#...     type = '1'
#...
#>>> print (test())
#<__main__.test object at 0x6ffff9c70b8>
#>>> print (test().type)
#1
#
class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True
#base class
class HeadingRule(Rule):
    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'
    # have \n len<=70 have : in ending block
class TitleRule(HeadingRule):
    type = 'title'
    first = True
    #this is initlized attribution, when we initial  TitleRule() in somewhere it the TitleRule() is an object and it hold a attribution first = True
    def condition(self, block):
        if not self.first: return False
        self.first = False
        #only first block can be title
        return HeadingRule,condition(self, block)
        #double check if it is head
class ListItemRule(Rule):
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self.block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True
    #identify leading - and remove it in block
class ListRule(ListItemRule):
    type = 'list'
    inside = False
    def condition(self, block):
        return True
    """  list structure
    block1
    -block2
    -block3
    block4
    list is from block1 to block2 so the condition is unknown we don't know if the block2 is '-block2' or 'block2', so the list rule's condition is all passing through
    """
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False
    #this function will feed all block to check if there is list in article.so it will not end rule matching until the block end.
    #other action will have start feed end, but list rule don't have feed so it will across block it won't end until you escape from block previous a non list block.
class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self, block):
        return True



        
