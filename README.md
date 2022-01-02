# Enigma-Plus
Python based Enigma machine simulator with some extra features

Example Usage 1:

#use preloaded enigma rotors.  ( there are not a lot loaded in yet)
rotor_3 = Enigma["III"]
rotor_2 = Enigma["II"]
rotor_1 = Enigma["I"]
reflector_A = rotors['reflector_B']

e = Enigma(rotors = [reflector_A,rotor_2,rotor_1,rotor_3])
message = "HEllO WORLD

cipher_text = "".join(e.cipher(letter) for letter in message)
    


#Example usage 2:

#create your own custom rotors.  Roters of different sizes and with multiple notches should work.
rotor_3 = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","BDFHJLCPRTXVZNYEIWGAKMUSQO",notch = [21])
rotor_2 = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","AJDKSIRUXBLHWTMCQGZNPYFVOE",notch = [4])
rotor_1 = Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","EKMFLGDQVZNTOWYHXUSPAIBRCJ",notch = [17])
reflector_A =Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ","EJMZALYXVBWFCRQUONTSPIKHGD",notch = [0])


e = Enigma(rotors = [reflector_A,rotor_2,rotor_1,rotor_3])
message = "HEllO WORLD

cipher_text = "".join(e.cipher(letter) for letter in message)


#Example Usage 3: 

#Create a generator to make enigma rotors with any character_set and any seed.  The character set must be an even numbered length for the reflector to word

roto_gen = Enigma.generate_rotor(character_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz .", seed = "enigma")

#this will generate 99 roters and 1 reflector utilizing the character set entered above

rotors = itertools.islice(roto_gen, 100)

e = Enigma(rotors=rotors)

message = "HEllO WORLD

cipher_text = "".join(e.cipher(letter) for letter in message)


