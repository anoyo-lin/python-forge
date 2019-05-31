def lines(file):
    for line in file: yield line
    yield '\n'
    #add \n at endline
def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            #remove space
            block.append(line)
            #insert every line into list
        elif block:
            yield ''.join(block).strip()
            #concatenate all line in a block w/o any space
            block = []
            #clear block to empty
