import random
import itertools

class Rotor():
   
    def __init__(self,inputs,outputs = None, notch = [0],ring = 0, next_rotor=None,  ):
        #need to raise an error if inputs are not even
        self.unlocked = False
        self.dial_index = 0
        self.ring = 0
        self._inputs = [x for x in inputs]
        self.notch = notch
        self.moved = False
        self._outputs = [x for x in outputs]
   
    @property
    def dial(self):  
        return self.dial_index
   
    @dial.setter
    def dial(self,i):
        self.dial_index = i%len(self._inputs)
    
    def forward(self,character): 
        index = self._inputs.index(character) 
        index +=self.dial
        index %=len(self._inputs)
        
        #Adjusts for the ring
        temp_output = self._outputs[-self.ring:] + self._outputs[:-self.ring] 
        temp_output = [self._inputs[(self._inputs.index(x)+self.ring)%len(self._inputs)] for x in temp_output]
        
        character = temp_output[index]
        index = self._inputs.index(character)
        index -=self.dial
        index %=len(self._inputs) 
        character = self._inputs[index]
        return character

    def reverse(self,character): 
        index = self._inputs.index(character) 
        index +=self.dial
        index %=len(self._inputs) 
        character = self._inputs[index]
        
        #Adjusts for the ring
        temp_output = self._outputs[-self.ring:] + self._outputs[:-self.ring] 
        temp_output = [self._inputs[(self._inputs.index(x)+self.ring)%len(self._inputs)] for x in temp_output]
        
        index = temp_output.index(character)
        index -=self.dial
        index %=len(self._inputs) 
        character = self._inputs[index]
        return character
        
class Enigma():
    
    rotors = {}
    rotors['VI'] = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","JPGVOUMFYQBENHZRDKASXLICTW",notch = [25,12])
    rotors['III'] = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","BDFHJLCPRTXVZNYEIWGAKMUSQO",notch = [21])
    rotors['II'] = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","AJDKSIRUXBLHWTMCQGZNPYFVOE",notch = [4])
    rotors['I'] = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","EKMFLGDQVZNTOWYHXUSPAIBRCJ",notch = [17])
    rotors['reflector_B'] = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","YRUHQSLDPXNGOKMIEBFZCWVJAT",notch = [0])
    rotors['reflector_A'] = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","EJMZALYXVBWFCRQUONTSPIKHGD",notch = [0])
    
    def __init__(self,rotors,seed = "enigma"):
        self.rotors = [x for x in rotors]
        self.base_character_set = self.rotors[0]._inputs
        random.seed(seed)
        
        self.set_jumpers()
        
    def advance_dials(self):
        last_rotor = self.rotors[-1]
        for i in range(1,len(self.rotors)-1):
            this_rotor = self.rotors[i]
            next_rotor = self.rotors[i+1]
            if next_rotor.moved and next_rotor.dial in next_rotor.notch:
                for j in range(i,len(self.rotors)-1):
                    self.rotors[j].dial+=1
                    self.rotors[j].moved= True
            else:
                this_rotor.moved = False 
        last_rotor.dial += 1
        last_rotor.moved = True
         
    def set_jumpers(self,letter_pairs=[]):
        self.jumpers = {letter:letter for letter in self.base_character_set }
        for pair in letter_pairs:
            self.jumpers[pair[0]] = pair[1]
            self.jumpers[pair[1]] = pair[0]
            
    def cipher(self,letter):
        if letter not in self.base_character_set:    #only will encipher characters in the character_set
            return letter
        self.advance_dials()    #advance the dial before cipher stuff

        letter = self.jumpers[letter] #start the jumpers

        for i in range(len(self.rotors)-1,0,-1):    #advances forward through the rotors
            letter = self.rotors[i].forward(letter)

        letter = self.rotors[0].forward(letter)    #bounces through the reflector

        for i in range(1,len(self.rotors)):     # advances reverse through the rotors
            letter = self.rotors[i].reverse(letter)

        letter = self.jumpers[letter] #start the jumpers
            
        return letter
    
    def cipher_text(self,text):
        return "".join(self.cipher(letter) for letter in text)
    
    @property
    def dials(self):
        return "|".join(self.base_character_set[self.rotors[i].dial] for i in range(1,len(self.rotors)))
    
    @dials.setter
    def dials(self,new_dial):
        new_dial = new_dial.split('|')
        for i in range(3,0,-1):
            rotor = self.rotors[i]
            rotor.dial=rotor._inputs.index(new_dial[i-1])
        self.rotors[0].dial = 0
           
    @property
    def rings(self):
        return "|".join(self.base_character_set[self.rotors[i].ring] for i in range(1,len(self.rotors)))
    @rings.setter
    def rings(self,new_rings):
        for index,ring in enumerate(new_rings.split('|')):
            rotor = self.rotors[index+1]
            rotor.ring = rotor._inputs.index(ring)
    @staticmethod       
    def generate_rotor(character_set="ABCDEFGHIJKLMNOPQRSTUVWXYZ",is_reflector = True, seed = None):
        while True:
            if seed != None:
                random.seed(seed)
            c = [x for x in character_set]   
            if is_reflector==True:
                is_reflector=False
                d = {}
                
                while len(d) < len(character_set):
                    choice_1 = c.pop(random.randint(0,len(c)-1))
                    choice_2 = c.pop(random.randint(0,len(c)-1))
                    d[choice_1]=choice_2
                    d[choice_2]=choice_1

                outputs = [d[x] for x in character_set]      
            elif outputs == None:
                outputs = self._inputs.copy()
                random.shuffle(self._outputs)
                
            yield Rotor(character_set,outputs,notch = [random.randint(0,len(character_set)-1)])
