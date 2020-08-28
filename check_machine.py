COM_CONFIG_end = 0xF0DA0001
COM_TMRS_RELOAD_start = 0xF0DA0010
COM_TMRS_RELOAD_end = 0xF0DA0011
COM_MEM0_READ_start = 0xF0DA0020
COM_MEM0_READ_end = 0xF0DA0021
COM_MEM1_READ_start = 0xF0DA0030
COM_MEM1_READ_end = 0xF0DA0031
COM_MEM0_WRITE_start = 0xF0DA0040
COM_MEM0_WRITE_end = 0xF0DA0041
COM_MEM1_WRITE_start = 0xF0DA0050
COM_MEM1_WRITE_end = 0xF0DA0051
COM_UART1_TRAN_CHECK_ok = 0xF0DA0060
COM_UART1_TRAN_CHECK_error = 0xF0DA0061
COM_UART2_TRAN_CHECK_ok = 0xF0DA0070
COM_UART2_TRAN_CHECK_error = 0xF0DA0071
COM_CHANNELS_READ_start = 0xF0DA0080
COM_CHANNELS_READ_end = 0xF0DA0081
COM_FTS_READ_start = 0xF0DA0090
COM_FTS_READ_end = 0xF0DA0091
COM_TLM_READ_start = 0xF0DA00A0
COM_TLM_READ_end = 0xF0DA00A1
COM_UART1_CONF_CHECK_start = 0xF0DA00B0
COM_UART1_CONF_CHECK_end = 0xF0DA00B1
COM_UART2_CONF_CHECK_start = 0xF0DA00C0
COM_UART2_CONF_CHECK_end = 0xF0DA00C1
COM_GPIO_CONF_CHECK_start = 0xF0DA00D0
COM_GPIO_CONF_CHECK_end = 0xF0DA00D1
COM_PLL_CONF_CHECK_start = 0xF0DA00E0
COM_PLL_CONF_CHECK_end = 0xF0DA00E1
COM_TMR1_CONF_CHECK_start = 0xF0DA00F0
COM_TMR1_CONF_CHECK_end = 0xF0DA00F1
COM_ALRMTMR_CONF_CHECK_start = 0xF0DA0100
COM_ALRMTMR_CONF_CHECK_end = 0xF0DA0101
COM_SPI_CONF_CHECK_start = 0xF0DA0110
COM_SPI_CONF_CHECK_end = 0xF0DA0111
COM_INMUX_CONF_CHECK_start = 0xF0DA0120
COM_INMUX_CONF_CHECK_end = 0xF0DA0121
COM_TSM_CONF_CHECK_start = 0xF0DA0130
COM_TSM_CONF_CHECK_end = 0xF0DA0131

COM_STAGE_0_start = 0xF0DA1000
COM_STAGE_0_end = 0xF0DA1001
COM_STAGE_1_start = 0xF0DA2000
COM_STAGE_1_end = 0xF0DA2001
COM_STAGE_2_start = 0xF0DA3000
COM_STAGE_2_end = 0xF0DA3001
COM_TMR1_IRQ_start = 0xF0DA4000
COM_TMR1_IRQ_end = 0xF0DA4001
COM_MEM_IRQ_start = 0xF0DA5000
COM_MEM_IRQ_end = 0xF0DA5001

COM_TIMEOUT = 0xF0DA6000
COM_MACHINE = 0xF0DA7000
COM_RAVE = 0xF0DA8000

THRESHOLD_ERRORS = 64
FILENAME = "U_20.08.2019_14-18-43.log"


def layout_reload(state, word, iter, count, word_num):
    print("{0:^8X} {1:^8X} {2:<4d} {3:<4d} {4:<4d}".format(state, word, iter, count, word_num))
    exit()


with open("logs/unsorting_logs/" + FILENAME, "r") as f:
    f_lines = f.readlines()
del f

lines = []
for line in f_lines:
    # if line[6:14] != " " * 8 and line[6:14] != "-" * 8 and line[6:14] != " Opcode ":
    #     lines.append(int(line[6:14], 16))
    if line[21:29] != " " * 8 and line[21:29] != "-" * 8 and line[21:29] != " Opcode ":
        lines.append(int(line[21:29], 16))

del f_lines

state = COM_CONFIG_end
state_prev = COM_CONFIG_end
state_prev2 = COM_CONFIG_end
flag_first_iter = 1
epoch_count = 0
flag_number_errors = 0
flag_errors = 0
errors_number = 0
errors_count = 0
flag_uart_error = 0
words_count = 0
flag_end_epoch = 0

count_temp = 0

for word in lines:
    words_count += 1

    if flag_uart_error == 1:
        flag_uart_error = 0

    elif flag_number_errors == 1:
        flag_number_errors = 0
        if word != 0:
            flag_errors = 1
            if word > THRESHOLD_ERRORS:
                errors_number = THRESHOLD_ERRORS
            else:
                errors_number = word

    elif flag_errors == 1 and errors_count < errors_number * 2:
        errors_count += 1

    else:
        errors_count = 0
        errors_number = 0
        flag_errors = 0
        
        state_prev3 = state_prev2
        state_prev2 = state_prev
        state_prev = state

        if state == COM_CONFIG_end:
            if word == state:
                state = COM_STAGE_0_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TMRS_RELOAD_start:
            if word == state:
                state = COM_TMRS_RELOAD_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TMRS_RELOAD_end:
            if word == state:
                count_temp += 1
                if epoch_count == 99:
                    epoch_count = 0
                else:
                    epoch_count += 1

                if state_prev3 == COM_STAGE_0_start:
                    if flag_first_iter == 1:
                        state = COM_MEM0_WRITE_start
                        flag_first_iter = 0
                    else:
                        state = COM_MEM1_READ_start

                elif state_prev3 == COM_STAGE_1_start:
                    state = COM_MEM0_READ_start

                elif state_prev3 == COM_STAGE_2_start:
                    state = COM_CHANNELS_READ_start

                else:
                    layout_reload(state, word, count_temp, epoch_count, words_count)
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM0_READ_start:
            if word == state:
                flag_number_errors = 1
                state = COM_MEM0_READ_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM0_READ_end:
            if word == state:
                if state_prev3 == COM_MEM0_WRITE_end:
                        state = COM_UART1_TRAN_CHECK_ok

                elif state_prev3 == COM_TMRS_RELOAD_end:
                    state = COM_MEM1_WRITE_start

                else:
                    layout_reload(state, word, count_temp, epoch_count, words_count)
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM1_READ_start:
            if word == state:
                flag_number_errors = 1
                state = COM_MEM1_READ_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM1_READ_end:
            if word == state:
                if state_prev3 == COM_TMRS_RELOAD_end:
                    state = COM_MEM0_WRITE_start

                elif state_prev3 == COM_MEM1_WRITE_end:
                    state = COM_UART1_TRAN_CHECK_ok
                
                else:
                    layout_reload(state, word, count_temp, epoch_count, words_count)
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM0_WRITE_start:
            if word == state:
                state = COM_MEM0_WRITE_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM0_WRITE_end:
            if word == state:
                state = COM_MEM0_READ_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM1_WRITE_start:
            if word == state:
                state = COM_MEM1_WRITE_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_MEM1_WRITE_end:
            if word == state:
                state = COM_MEM1_READ_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_UART1_TRAN_CHECK_ok:
            if word == state:
                state = COM_UART2_TRAN_CHECK_ok
            elif word == COM_UART1_TRAN_CHECK_error:
                state = COM_UART2_TRAN_CHECK_ok
                flag_uart_error = 1
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        # elif state == COM_UART1_TRAN_CHECK_error:

        elif state == COM_UART2_TRAN_CHECK_ok:
            if word == state:
                if state_prev3 == COM_MEM0_READ_end:
                    state = COM_STAGE_0_end
                elif state_prev3 == COM_MEM1_READ_end:
                    state = COM_STAGE_1_end

                elif state_prev3 == COM_TSM_CONF_CHECK_end:
                    state = COM_STAGE_2_end
                else:
                    layout_reload(state, word, count_temp, epoch_count, words_count)
            elif word == COM_UART2_TRAN_CHECK_error:
                flag_uart_error = 1
                if state_prev3 == COM_MEM0_READ_end:
                    state = COM_STAGE_0_end
                elif state_prev3 == COM_MEM1_READ_end:
                    state = COM_STAGE_1_end

                elif state_prev3 == COM_TSM_CONF_CHECK_end:
                    state = COM_STAGE_2_end
                else:
                    layout_reload(state, word, count_temp, epoch_count, words_count)
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        # elif state == COM_UART2_TRAN_CHECK_error:

        elif state == COM_CHANNELS_READ_start:
            if word == state:
                flag_number_errors = 1
                state = COM_CHANNELS_READ_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_CHANNELS_READ_end:
            if word == state:
                state = COM_FTS_READ_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_FTS_READ_start:
            if word == state:
                flag_number_errors = 1
                state = COM_FTS_READ_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_FTS_READ_end:
            if word == state:
                state = COM_TLM_READ_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TLM_READ_start:
            if word == state:
                flag_number_errors = 1
                state = COM_TLM_READ_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TLM_READ_end:
            if word == state:
                state = COM_UART1_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_UART1_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_UART1_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_UART1_CONF_CHECK_end:
            if word == state:
                state = COM_UART2_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_UART2_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_UART2_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_UART2_CONF_CHECK_end:
            if word == state:
                state = COM_GPIO_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_GPIO_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_GPIO_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_GPIO_CONF_CHECK_end:
            if word == state:
                state = COM_PLL_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_PLL_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_PLL_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_PLL_CONF_CHECK_end:
            if word == state:
                state = COM_TMR1_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TMR1_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_TMR1_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TMR1_CONF_CHECK_end:
            if word == state:
                state = COM_ALRMTMR_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_ALRMTMR_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_ALRMTMR_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_ALRMTMR_CONF_CHECK_end:
            if word == state:
                state = COM_SPI_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_SPI_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_SPI_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_SPI_CONF_CHECK_end:
            if word == state:
                state = COM_INMUX_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_INMUX_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_INMUX_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_INMUX_CONF_CHECK_end:
            if word == state:
                state = COM_TSM_CONF_CHECK_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TSM_CONF_CHECK_start:
            if word == state:
                flag_number_errors = 1
                state = COM_TSM_CONF_CHECK_end
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TSM_CONF_CHECK_end:
            if word == state:
                state = COM_UART1_TRAN_CHECK_ok
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_STAGE_0_start:
            if word == state:
                state = COM_TMRS_RELOAD_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_STAGE_0_end:
            flag_end_epoch = 1
            if word == state:
                state = COM_STAGE_2_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_STAGE_1_start:
            if word == state:
                state = COM_TMRS_RELOAD_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_STAGE_1_end:
            flag_end_epoch = 1
            if word == state:
                state = COM_STAGE_2_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_STAGE_2_start:
            if word == state:
                state = COM_TMRS_RELOAD_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_STAGE_2_end:
            flag_end_epoch = 1
            # print(words_count)
            if word == state:
                if epoch_count == 0:
                    state = COM_STAGE_0_start
                elif epoch_count == 50:
                    state = COM_STAGE_1_start
                else:
                    state = COM_STAGE_2_start
            else:
                layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TMR1_IRQ_start:
            layout_reload(state, word, count_temp, epoch_count, words_count)

        elif state == COM_TMR1_IRQ_end:
            state = COM_STAGE_0_start

        # elif state == COM_MEM_IRQ_start:

        # elif state == COM_MEM_IRQ_end:

        else:
            layout_reload(state, word, count_temp, epoch_count, words_count)
