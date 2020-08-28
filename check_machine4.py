FILENAME = "U_23.08.2019_12-38-34.log"

filename = "logs/unsorting_logs/" + FILENAME
length = sum(1 for l in open(filename, "r"))

first_hit = False
counter = None

with open(filename, "r") as f:
    for i in range(length):
        opcode = f.readline()[28:36]

        if counter is None:
            counter = int(opcode, 16)

        if first_hit is False and int(opcode, 16) != counter:
            counter = int(opcode, 16)
            first_hit = True

        # if (counter - 1) % 50 == 0 and counter != 1:
        #     counter += 1

        if counter != int(opcode, 16):
            print(i, opcode, counter, int(opcode, 16))
            exit()

        counter += 1
print("END", counter)
