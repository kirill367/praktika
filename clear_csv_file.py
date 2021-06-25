with open('zoo.csv') as inp, open('cleared_zoo4.csv', 'w') as out:
    out.write(inp.read().replace('�', 'EEEEE'))