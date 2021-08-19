import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        

alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
sub = [ 22,   8,   2,   31, 11,   5,   5,   2,   1,   3,   4,   4,   3]

for char in alph:
    createFolder(f"./TR.{char}/")
    
for char, number in zip(alph, sub):
    for i in range(1, number + 1):
        createFolder(f"TR.{char}/TR.{char}.{i}")