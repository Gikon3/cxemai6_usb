FILENAME = "U_21.08.2019_13-59-51.log"

filename = "logs/unsorting_logs/" + FILENAME
length = sum(1 for l in open(filename, "r"))

flag_numeric = False
flag_numeric2 = False
flag = 0
counter = 2

with open(filename, "r") as f:
    for i in range(length):
        line = f.readline()

        opcode = line[21:29]

        if flag_numeric is True:
            if int(opcode, 16) != counter:
                print(i, counter, opcode, int(opcode, 16))
                exit()
            flag = 1
            flag_numeric = False
        elif flag_numeric2 is True:
            if int(opcode, 16) != counter:
                print(i, counter, opcode, int(opcode, 16))
                exit()
            counter += 1
            flag_numeric2 = False
            flag = 0
        elif opcode == "f0da9000":
            if flag == 0:
                flag_numeric = True
            elif flag == 1:
                flag_numeric2 = True

        if (counter - 1) % 50 == 0 and counter != 1:
            counter += 1

print(counter)
