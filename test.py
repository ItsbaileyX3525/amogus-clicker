from ursina import *

app = Ursina()

sequence = []

def input(key):
    global sequence
    
    if key.isalpha():
        sequence.append(key.lower())
        
        if "".join(sequence) == "hello":
            print("sex")
            sequence = [] 
            
    else:
        sequence = []

app.run()
