import sys

text = sys.stdin.readlines()
text = [line.strip() for line in text if line.strip()]

l = len(text)

variables = []
j = 0
while text[j].startswith('var') == 1:
    var = text[j].strip('var').strip()
    if var in variables:
        print("SYNTAX ERROR: A variable cannot be declared twice.")
        exit(0)
    variables.append(var)
    del (text[j])
labels = []
addr = text.copy()

A = {'add': '00000', 'sub': '00001', 'mul': '00110',
     'xor': '01010', 'or': '01011', 'and': '01100'}
B = {'mov': '00010', 'rs': '01000', 'ls': '01001'}
C = {'mov': '00011', 'div': '00111', 'not': '1101', 'cmp': '01110'}
D = {'ld': '00100', 'st': '00101'}
E = {'jmp': '01111', 'jlt': '11100', 'jgt': '11101', 'je': '11111'}
F = {'hlt': '11010'}

reg_encoding = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011',
                'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}

lbl_addr = {}
for i in range(len(addr)):
    if addr[i].split()[0].endswith(':'):
        if addr[i].split()[0] in labels:
            print(
                "SYNTAX ERROR: Defining routine for a label multiple times is not permitted.")
            exit(0)
        lbl_addr[addr[i].split()[0].rstrip(":")] = bin(i).lstrip('0b')
        labels.append(addr[i].split()[0].rstrip(":"))
        addr[i] = addr[i].lstrip(addr[i].split()[0].lstrip())
        addr[i] = addr[i].lstrip()
    elif addr[i].split()[0] in E:
        if addr[i].split()[1] in labels:
            print(
                "SYNTAX ERROR: Defining routine for a label multiple times is not permitted.")
            exit(0)
        lbl_addr[addr[i].split()[1].rstrip(":")] = bin(i).lstrip('0b')
        labels.append(addr[i].split()[1].rstrip(":"))


text_len = len(text)


def binary_code(ins, text_len):

    s = ins.split()
    if s[0] in A:
        if (s[1] or s[2] or s[3]) not in reg_encoding:
            print("SYNTAX ERROR: Typos in Register Name.")
            exit(0)
        if (s[2] or s[3]) == 'FLAGS':
            print("SYNTAX ERROR: Illegal use of FLAGS.")
            exit(0)
        return (A[s[0]]+'00'+reg_encoding[s[1]]+reg_encoding[s[2]]+reg_encoding[s[3]]), text_len
    elif s[0] == 'mov':
        if s[2].startswith('$'):
            imm = int(s[2].lstrip('$'))
            if (imm < 0 or imm > 127):
                print("SYNTAX ERROR: Illegal Immdiate Value.")
                exit(0)
            imm = bin(imm)
            imm = imm.lstrip('0b')
            imm = '0'*(7-len(imm))+imm
            if s[1] not in reg_encoding:
                print("SYNTAX ERROR: Typos in Register Name.")
                exit(0)
            return (B[s[0]]+'0'+reg_encoding[s[1]]+imm), text_len
        elif s[2].isdigit():
            print("SYNTAX ERROR: '"+s[2]+"' not defined.")
            exit(0)
        else:
            if (s[1] or s[2]) not in reg_encoding:
                print("SYNTAX ERROR: Typos in Register Name.")
                exit(0)
            return (C[s[0]]+'00000'+reg_encoding[s[1]]+reg_encoding[s[2]]), text_len
    elif s[0] in B:
        if s[2].startswith('$') == True:
            print("SYNTAX ERROR: '"+s[2]+"' not defined.")
            exit(0)
        imm = int(s[2].lstrip('$'))
        if (imm < 0 or imm > 127):
            print("SYNTAX ERROR: Illegal Immdiate Value.")
            exit(0)
        imm = bin(imm)
        imm = imm.lstrip('0b')
        imm = '0'*(7-len(imm))+imm
        if s[1] not in reg_encoding:
            print("SYNTAX ERROR: Typos in Register Name.")
            exit(0)
        if s[1] == 'FLAGS':
            print("SYNTAX ERROR: Illegal use of FLAGS.")
            exit(0)
        return (B[s[0]]+'0'+reg_encoding[s[1]]+imm), text_len
    elif s[0] in C:
        if (s[1] or s[2]) not in reg_encoding:
            print("SYNTAX ERROR: Typos in Register Name.")
            exit(0)
        if s[1] == 'FLAGS':
            print("SYNTAX ERROR: Illegal use of FLAGS.")
            exit(0)
        return (C[s[0]]+'00000'+reg_encoding[s[1]]+reg_encoding[s[2]]), text_len
    elif s[0] in D:
        if s[1] not in reg_encoding:
            print("SYNTAX ERROR: Typos in Register Name.")
            exit(0)
        if s[2]+':' in labels:
            print("SYNTAX ERROR: Misuse of label as variable.")
            exit(0)
        if s[2] not in variables:
            print("SYNTAX ERROR: Use of undefined variables.")
            exit(0)
        var_addr = bin(text_len)
        var_addr = var_addr.lstrip('0b')
        var_addr = '0'*(7-len(var_addr))+var_addr
        text_len += 1
        return (D[s[0]]+'0'+reg_encoding[s[1]]+var_addr), text_len
    elif s[0] in E:
        if s[1] in variables:
            print("SYNTAX ERROR: Misuse of variable as label.")
            exit(0)
        if (s[1]) not in labels:
            print("SYNTAX ERROR: Use of undefined labels.")
            exit(0)
        label_addr = lbl_addr[s[1]]
        label_addr = '0'*(7-len(label_addr))+label_addr
        return (E[s[0]]+'0000'+label_addr), text_len
    elif s[0] in F:
        return (F[s[0]]+'00000000000'), text_len
    elif s[0] == 'var':
        print("SYNTAX ERROR: var not declared at beginning.")
        exit(0)
    else:
        print("SYNTAX ERROR: Typos in Instruction Name.")
        exit(0)


f1 = open('output.txt', 'w')
for i in addr:
    line, text_len = binary_code(i, text_len)
    sys.stdout.write(line+'\n')
    if i == 'hlt':
        break

if addr[-1] != "hlt":
    print("SYNTAX ERROR: hlt not being used as last instruction.")
    exit(0)
if i != 'hlt':
    print("SYNTAX ERROR: Missing hlt instruction.")
    exit(0)
f1.close()
