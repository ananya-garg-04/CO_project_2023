import sys
text = sys.stdin.readlines()
# f2 = open("CO_A_P1/SimpleSimulator/test1.txt","r")
# f=open("test.txt","w")
# text=.readlines()
# f.close()
text = [line.strip() for line in text if line.strip()]

l = len(text)
#print(text)

reg_encoding={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS",}
#Register values
reg_val={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":0}

A = { '00000':'add',  '00001':'sub', '00110' :'mul',
      '01010':'xor',  '01011':'or',  '01100':'and'}
B = { '00010':'mov',  '01000':'rs',  '01001':'ls'}
C = {'00011':'mov',  '00111':'div',  '01101':'not',  '01110':'cmp'}
D = {'00100':'ld',  '00101':'st'}
E = { '01111':'jmp',  '11100':'jlt',  '11101':'jgt',  '11111':'je'}
F = {'11010':'hlt'}

memory=text.copy()
for i in range(128-l):
    memory.append("0"*16)
V,L,G,e = "0","0","0","0"
program_counter=0
halted=False

def print_pc():
    binpc = bin(program_counter)
    binpc = str(binpc).lstrip("0b")
    len_binpc = len(binpc)
    len_binpc = 7 - len_binpc
    s = str(len_binpc*"0")+str(binpc)+str(" "*8)
    sys.stdout.write(s)
    # sys.stdout.write(s)

def print_flag():
    s = str("")+str("0"*12)+str(V)+str(L)+str(G)+str(e)
    sys.stdout.write(s)
def print_reg_values():
    
    for reg in reg_val:
        if reg=="FLAGS":
            print_flag()
            return
        binval = (bin(reg_val[reg]))
        registervalue = (str(binval).lstrip("0"))
        registervalue = registervalue.lstrip("b")
        len_regval = len(str(registervalue))
        # print(len_regval)
        len_regval = 16 - len_regval
        s = len_regval*"0"+str(registervalue)+" "
        sys.stdout.write(s)
        # sys.stdout.write(s)
        
while(halted == False):
    for i in range(l):
        line=text[i]
        ins=line[0:5]
        if ins in A:
            unused=line[5:7]
            reg1=line[7:10]
            reg2=line[10:13]
            reg3=line[13::]
            if ins=='00000':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]+reg_val[reg_encoding[reg3]]
                if reg_val[reg_encoding[reg1]]<0 or reg_val[reg_encoding[reg1]]>127:
                    V="1"
                print_pc()
                program_counter+=1
                
                print_reg_values()
            elif ins=='00001':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]-reg_val[reg_encoding[reg3]]
                if reg_val[reg_encoding[reg1]]<0 or reg_val[reg_encoding[reg1]]>127:
                    V="1"
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='00110':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]*reg_val[reg_encoding[reg3]]
                if reg_val[reg_encoding[reg1]]<0 or reg_val[reg_encoding[reg1]]>127:
                    V="1"
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='01010':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]^reg_val[reg_encoding[reg3]]
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='01011':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]|reg_val[reg_encoding[reg3]]
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='01100':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]&reg_val[reg_encoding[reg3]]
                print_pc()
                program_counter+=1
                print_reg_values()
        elif ins in B:
            unused=line[5:6]
            reg1=line[6:9]
            imm=line[9::]
            imm=int(imm)
            decimal, i = 0, 0
            while(imm != 0):
                dec = imm % 10
                decimal = decimal + dec * pow(2, i)
                imm = imm//10
                i += 1
            imm=decimal
            if ins=='00010':
                reg_val[reg_encoding[reg1]]=imm
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='01000':
                reg_val[reg_encoding[reg1]]/=(2**imm)
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='01001':
                reg_val[reg_encoding[reg1]]*=(2**imm)
                print_pc()
                program_counter+=1
                print_reg_values()
        elif ins in C:
            unused=line[5:10]
            reg1=line[10:13]
            reg2=line[13::]
            if ins=='00011':
                reg_val[reg_encoding[reg1]]=reg_val[reg_encoding[reg2]]
                print_pc()
                program_counter+=1
                print_reg_values()
            elif ins=='00111':
                if reg_val[reg_encoding[reg2]]!=0:
                    reg_val["R0"]=reg_val[reg_encoding[reg1]]//reg_val[reg_encoding[reg2]]
                    reg_val["R1"]=reg_val[reg_encoding[reg1]]%reg_val[reg_encoding[reg2]]
                if reg_val[reg_encoding[reg2]]==0:
                    V='1'
                    reg_val["R0"]=0
                    reg_val["R1"]=0
                print_reg_values()
                print_pc()
                program_counter+=1
            elif ins=='01110':
                if reg_val[reg_encoding[reg1]]<reg_val[reg_encoding[reg2]]:
                    L='1'
                elif reg_val[reg_encoding[reg1]]>reg_val[reg_encoding[reg2]]:
                    G='1'
                elif reg_val[reg_encoding[reg1]]==reg_val[reg_encoding[reg2]]:
                    e='1'
                print_reg_values()
                print_pc()
                program_counter+=1
            elif ins=='01101':
                reg_val[reg_encoding[reg1]]=~reg_val[reg_encoding[reg2]]
                print_reg_values()
                print_pc()
                program_counter+=1
        elif ins in D:
            unused=line[5:6]
            reg1=line[6:9]
            mem=line[9::]
            mem=int(mem)
            decimal, i = 0, 0
            while(mem != 0):
                dec = mem % 10
                decimal = decimal + dec * pow(2, i)
                mem = mem//10
                i += 1
            mem=decimal
            val=(int(memory[mem]))
            decimal, i = 0, 0
            while(val != 0):
                dec = val % 10
                decimal = decimal + dec * pow(2, i)
                val = val//10
                i += 1
            val=decimal
            if ins=='00100':
                reg_val[reg_encoding[reg1]]=val
                print_reg_values()
                print_pc()
                program_counter+=1
            elif ins=='00101':
                val=reg_val[reg_encoding[reg1]]
                val=bin(val)
                val=val.lstrip('0')
                val=val.lstrip('b')
                diff = 16 - len(str(val))
                val = diff*"0"+str(val)
                memory[mem]=val
                print_pc()
                print_reg_values()
                
                program_counter+=1
        elif ins in E:
            unused=line[5:9] 
            mem=line[9::]
            mem=int(mem)
            if ins == "01111":
                program_counter = mem
                print_reg_values()
                print_pc()

            elif ins == "11100" :
                if(L=="1"):
                    program_counter = int("0b"+mem,2)
                    print_reg_values()
                    print_pc()
            elif ins == "11101":
                if(G=="1"):
                    program_counter = mem
                    print_reg_values()
                    print_pc()
            elif ins == "11111":
                if(e=="1"):
                    program_counter = int("0b"+mem,2)
                    print_reg_values()
                    print_pc()

        elif ins in F:
            halted = True
            print_pc()
            print_reg_values()
            # f.write("\n")
            sys.stdout.write("\n")
            for i in memory:
                sys.stdout.write(str(i))
            
                # sys.stdout.write(i)
                sys.stdout.write("\n")
            # print(memory)
            # for i in range(l):

            #     # print_pc()
            #     print_reg_values()
            # for i in memory:
            #     # print(i)
            exit(0)
        sys.stdout.write("\n")
    


