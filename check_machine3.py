FILENAME = "U_23.08.2019_13-50-12.log"

COM_UART1_TRAN_CHECK_error = "f0da0061"
COM_UART2_TRAN_CHECK_error = "f0da0071"

COM_OK = "f0da7000"
COM_STM_START = "f0daf000"
COM_FLAG_ERROR = "f0dae000"

filename = "logs/unsorting_logs/" + FILENAME
length = sum(1 for l in open(filename, "r"))

flag_number_epoch = False
number_epoch = None
flag_reg = False
flag_uart = False
flag_number_errors = False

with open(filename, "r") as f:
    for i in range(length):
        opcode = f.readline()[28:36]
        # line = f.readline()
        # opcode = line[21:23] + line[24:26] + line[27:29] + line[30:32]
        # opcode = opcode.lower()

        if flag_uart is True:
            flag_uart = False

        elif flag_number_errors is True:
            print(i, "error")
            exit()

        elif flag_reg is True:
            flag_reg = False
            if opcode == COM_UART1_TRAN_CHECK_error or opcode == COM_UART2_TRAN_CHECK_error:
                flag_uart = True
            else:
                flag_number_errors = True
            if opcode == COM_UART2_TRAN_CHECK_error:
                number_epoch += 1

        elif flag_number_epoch is True:
            flag_number_epoch = False
            flag_reg = True
            if int(opcode, 16) == number_epoch:
                pass
            elif number_epoch is None:
                number_epoch = int(opcode, 16)
            else:
                print(i, int(opcode, 16), number_epoch, opcode, "number epoch")
                exit()

        elif opcode == COM_STM_START:
            pass

        elif opcode == COM_OK:
            pass

        elif opcode == COM_FLAG_ERROR:
            flag_number_epoch = True

        else:
            # print(i, opcode)
            pass

print(i, "END")
