class Handler:
        def callback(self, prefix, name, *args):
            #*args will collect the extra parameter
            method = get_attr(self, prefix+name, None)
            #get_attr(object, method_name, null_return_value)
            #method is a kind of object, so it can return a function that initialized fun() func(*args)
            if callable(method): return method(*args)
            #if callable return the funtion, if it has extra parameter it will return it with that parameter
        def start(self, name):
            result = self.callback('start_', name)
        def end(self, name):
            result = self.callback('end_', name)
        def sub(self, name):
            def substitution(match):
                result = self.callback('sub_', name, match)
                if result is None: result = match.group(0)
                #set default whole pre-match raw pattern
                return result
                #return sub_xxx(match)
            return substitution
        #re.sub can let a function as secondary parameter, and it is the replacement function, so it won't set match as the parameter in sub function, and let substitution more abstractive to omit the match patttern in it, and also it will be utilized that re.sub(match_pattern, object.sub(xxx), file). object.sub(xxx) return a function not  initilized. substitution(match) we don't know match until we have an object.

#this is base class

class HTMLRenderer(Handler):
    #a subclass inherit from Handler
    def start_document(self):
        print('<html><head><title>...</title></head><body>')
    def end_document(self):
        print('</body></html>')
    def start_paragraph(self):
        print('<p>')
    def end_paragraph(self):
        print('</p>')
    def start_heading(self):
        print('<h2>')
    def end_heading(self):
        print('</h2>')
    def start_list(self):
        print('<ul>')
    def end_list(self):
        print('</ul>')
    def start_listitem(self):
        print('<li>')
    def end_listitem(self):
        print('</li>')
    def start_title(self):
        print('<h1>')
    def end_title(self):
        print('</h1>')
    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))
    #i dont know why the sub function will use return instead print.
    #print will render the textline now, and return text will tansfer it into a function used by re.sub
    def sub_url(self, match):
        return '<a href="{0}">{1}</a>'.format(match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:{0}">{1}</a>'.format(match.group(1), match.group(1))
    def feed(self, data)
        return data

