#this takes the value you input and finds the key it coresponds to.
def inv(dic,goal):
    for key,value in dic.items():
        if value == goal:
            return key
#this is to turn a string into a dictionary
def str_to_dic(string):
    dic=dic_zip(base_string,string)
    return dic
#takes a string of keys and a string of values and turns it into a dictionary where the first key referances the first value
def dic_zip(keys, values):
    dic = {}
    for i in range(len(keys)):
        dic[keys[i]] = values[i]
    return dic
#takes the pairs the user inputs as the plug board settings and turns it into a dictionary.
def plug_to_dic(string):
    keys=[]
    values=[]
    str_array=[]
    str_array=string.split(" ")
    for item in str_array:
        keys.append(item[0])
        keys.append(item[1])
        values.append(item[1])
        values.append(item[0])
    dic=dic_zip(keys,values)
    for char in base_string:
        if dic.get(char)==None:
            dic[char]=char
    return dic
import sys
#this section is all formating and rearanging data and some input valadation
base_string="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number_list=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
rotorstr=["EKMFLGDQVZNTOWYHXUSPAIBRCJ","AJDKSIRUXBLHWTMCQGZNPYFVOE","AJDKSIRUXBLHWTMCQGZNPYFVOE","ESOVPZJAYQUIRHXLNFTGKDCMWB","VZBRGITYUPSDNHLXAWMJQOFECK","JPGVOUMFYQBENHZRDKASXLICTW","NZJHGRCXMYSWBOUFAIVLPEKQDT","FKQHTLXOCBJSPDZRAMEWNIUYGV"]
reflectstr=["EJMZALYXVBWFCRQUONTSPIKHGD","YRUHQSLDPXNGOKMIEBFZCWVJAT","FVPJIAOYEDRZXWGCTKUQSBNMHL"]
rotor_kick={1:"Q",2:"E",3:"V",4:"J",5:"Z"}
num_letter_dic=str_to_dic(number_list)
rotordic=[]
reflectdic=[]
the_line=[]
coded_message=[]
plug_dic={}
reflector_transfer={"a":0,"b":1,"c":2}
skip=0
for item in rotorstr:
    rotordic.append(str_to_dic(item))
for item in reflectstr:
    reflectdic.append(str_to_dic(item))
message_file=open("in_message.txt","r")
plug_str=message_file.readline()
plug_dic=plug_to_dic(plug_str)
used_rotors=message_file.readline()
used_rotors=used_rotors.split(" ")
for i in range(3):
    used_rotors[i]=int(used_rotors[i])
    while used_rotors[i]<1 or used_rotors[i]>5:
        print("there are only 5 rotors")
        used_rotors=int(input("what is your new rotor for rotor " + str(i)))
while used_rotors[3] not in ["a","b","c"]:
    used_rotors[3]=input("the reflector must be a, b or c. what reflector do you want to use : ")

rotor_positions=message_file.readline()
rotor_positions=rotor_positions.split(" ")
for i in range(3):
    if i==2:
        rotor_positions[i]=rotor_positions[i][0:2]
    rotor_positions[i]=int(rotor_positions[i])
    while rotor_positions[i]<1 or rotor_positions[i]>26:
        question =("The rotor position must be a number between 1 and 26. What rotor position do you want for rotor " + str(i+1) + ": ")
        rotor_positions[i]=int(input(question))
ring_settings=message_file.readline()
ring_settings=ring_settings.split(" ")
del(ring_settings[3])
for i in range(3):
    ring_settings[i]=int(ring_settings[i])
    while ring_settings[i]<1 or ring_settings[i]>26:
        question="The ring setting must be a number between 1 and 26. What ring setting do you want for rotor " + str(i+1) + ": ")
        ring_settings[i]=int(input(question))
    rotor_positions[i]=rotor_positions[i]-ring_settings[i]%26
#this starts the part of the program which encodes the message
message=message_file.readlines()
for line in message:
    for char in line:
        if char=="\n":
            the_line.append(char)
        elif char==" ":
            skip=0
        elif skip>=1:
            skip=skip-1
        else:
            #incriments the first rotor
            rotor_positions[1]+=rotor_positions[1]
            #if rotors pass the kick over position then this code turns the next rotor 1 place
            for i in range(2):
                if rotor_positions[i]==(num_letter_dic[rotor_kick[int( used_rotors[i])]]+1+ring_settings[i])%26:
                    rotor_positions[i+1]+=rotor_positions[i+1]
            #sends the message through the plug board
            char=plug_dic[char]
            #sends the message through the rotors lines 1 and 3 in the loop apply the rotation of the rotors
            for i in range(3):
                char=base_string[(num_letter_dic[char]+int(rotor_positions[i]))%26]
                char=rotordic[int(used_rotors[i])][char]
                char=base_string[(num_letter_dic[char]-int(rotor_positions[i]))%26]
            #sends the message back through the reflector
            char=reflectdic[reflector_transfer[used_rotors[3]]][char]
            #sends the message through the rotors
            for i in range(2,-1,-1):
                char=base_string[(num_letter_dic[char]+int(rotor_positions[i]))%26]
                char=inv(rotordic[int(used_rotors[i])],char)
                char=base_string[(num_letter_dic[char]-int(rotor_positions[i]))%26]
            #sends the message back through the plug board
            char=plug_dic[char]
            print(char)
            #adds the encoded charicter to the current line.
            the_line.append(char)
    #turns the list of charicters into a string and adds it to the list of lines for the coded message
    coded_message.append("".join(the_line))
    #clears the line
    the_line=[]
#opens the file for the coded message
message_out=open("out_message.txt","w")
#turns the list of lines into a string
coded_message="".join(coded_message)
#writes the string to the file for the encoded message
message_out.write(coded_message)
#closes the files
message_file.close()
message_out.close()
