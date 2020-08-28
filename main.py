import datetime
import time
import curses
import ComPort
import PrintMessage
import CountErrors

PORTNAME = "COM3"
THRESHOLD_ERRORS = 64

COM_CONFIG_end = "F0DA0001"
COM_TMRS_RELOAD_start = "F0DA0010"
COM_TMRS_RELOAD_end = "F0DA0011"
COM_MEM0_READ_start = "F0DA0020"
COM_MEM0_READ_end = "F0DA0021"
COM_MEM1_READ_start = "F0DA0030"
COM_MEM1_READ_end = "F0DA0031"
COM_MEM0_WRITE_start = "F0DA0040"
COM_MEM0_WRITE_end = "F0DA0041"
COM_MEM1_WRITE_start = "F0DA0050"
COM_MEM1_WRITE_end = "F0DA0051"
COM_UART1_TRAN_CHECK_ok = "F0DA0060"
COM_UART1_TRAN_CHECK_error = "F0DA0061"
COM_UART2_TRAN_CHECK_ok = "F0DA0070"
COM_UART2_TRAN_CHECK_error = "F0DA0071"
COM_CHANNELS_READ_start = "F0DA0080"
COM_CHANNELS_READ_end = "F0DA0081"
COM_FTS_READ_start = "F0DA0090"
COM_FTS_READ_end = "F0DA0091"
COM_TLM_READ_start = "F0DA00A0"
COM_TLM_READ_end = "F0DA00A1"""
COM_UART1_CONF_CHECK_start = "F0DA00B0"
COM_UART1_CONF_CHECK_end = "F0DA00B1"
COM_UART2_CONF_CHECK_start = "F0DA00C0"
COM_UART2_CONF_CHECK_end = "F0DA00C1"
COM_GPIO_CONF_CHECK_start = "F0DA00D0"
COM_GPIO_CONF_CHECK_end = "F0DA00D1"
COM_PLL_CONF_CHECK_start = "F0DA00E0"
COM_PLL_CONF_CHECK_end = "F0DA00E1"
COM_TMR1_CONF_CHECK_start = "F0DA00F0"
COM_TMR1_CONF_CHECK_end = "F0DA00F1"
COM_ALRMTMR_CONF_CHECK_start = "F0DA0100"
COM_ALRMTMR_CONF_CHECK_end = "F0DA0101"
COM_SPI_CONF_CHECK_start = "F0DA0110"
COM_SPI_CONF_CHECK_end = "F0DA0111"
COM_INMUX_CONF_CHECK_start = "F0DA0120"
COM_INMUX_CONF_CHECK_end = "F0DA0121"
COM_TSM_CONF_CHECK_start = "F0DA0130"
COM_TSM_CONF_CHECK_end = "F0DA0131"

COM_STAGE_0_start = "F0DA1000"
COM_STAGE_0_end = "F0DA1001"
COM_STAGE_1_start = "F0DA2000"
COM_STAGE_1_end = "F0DA2001"
COM_STAGE_2_start = "F0DA3000"
COM_STAGE_2_end = "F0DA3001"
# COM_TMR1_IRQ_start = "F0DA4000"
# COM_TMR1_IRQ_end = "F0DA4001"
COM_MEM_IRQ_start = "F0DA5000"
COM_MEM_IRQ_end = "F0DA5001"

COM_UNRESET_DEVICE = "F0DA6000"
COM_OK = "F0DA7000"
COM_ALRM_TMR = "F0DA8000"
COM_ERR2_MEM = "F0DA9000"
COM_err_CORR_IRQ = "F0DA9100"
COM_TMR1_IRQ = "F0DAA000"
COM_TIMEOUT_SPI = "F0DAB000"
COM_RAVE = "F0DAC000"
COM_MACHINE = "F0DAD000"
COM_FLAG_ERROR = "F0DAE000"
COM_STM_START = "F0DAF000"
COM_BUFFER_FILL = "F0DAF100"

print_mes = PrintMessage.PrintMessage()
com_port = ComPort.ComPort(portname=PORTNAME)

flag_number_errors = False
flag_rave_expected = False
flag_rave_error = False
flag_errors = False
flag_epoch_num = False
flag_irq_memory_addr = False
flag_irq_memory_word = False
number_errors = 0
count_errors = 0

win = curses.initscr()
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addstr(3, 2, "Configuration:")
win.addstr(3, 22, "IRQ:")
win.addstr(10, 22, "Events:")
win.addstr(18, 2, "Transaction:")
win.addstr(26, 2, " -- To Exit, press ESC -- ")

errors = CountErrors.CountErrors()
last_epoch = 0
invalid_opcode = 0
timeout_uart = 0
buffer_fill = 0
key = 0

start_time = time.time()
try:
    while key != 27:
        key = win.getch()

        win.addstr(1, 2, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        win.addstr(1, 24, "{0:.0f} seconds".format(time.time() - start_time))

        i = 4
        for name, value in errors.errors_count_config.items():
            win.addstr(i, 4, "{0:<8s} {1:<4d}".format(name, value))
            i += 1

        i = 4
        for name, value in errors.irq_count.items():
            win.addstr(i, 24, "{0:<8s} {1:<4d}".format(name, value))
            i += 1

        i = 11
        for name, value in errors.event_count.items():
            win.addstr(i, 24, "{0:<15s} {1:<4d}".format(name, value))
            i += 1

        i = 19
        for name, value in errors.tran_count.items():
            win.addstr(i, 4, "{0:<5s} {1:<4d}".format(name, value))
            i += 1

        win.addstr(22, 22, "{0:<14s} {1:<6d}".format("Buffer fill", buffer_fill))
        win.addstr(23, 22, "{0:<14s} {1:<6d}".format("Invalid OPCODE", invalid_opcode))
        win.addstr(24, 2, "{0:<10s} {1:<6d}".format("Last Epoch", last_epoch))
        win.addstr(24, 22, "{0:<14s} {1:<6d}".format("Timeout UART", timeout_uart))

        data = com_port.read(flag_errors or flag_number_errors or flag_rave_error or flag_rave_expected
                             or flag_irq_memory_addr or flag_irq_memory_word or flag_epoch_num)

        if data == COM_STM_START or data == COM_BUFFER_FILL or data == COM_CONFIG_end or data == COM_ALRM_TMR \
                or data == COM_ERR2_MEM or data == COM_err_CORR_IRQ or data == COM_TMR1_IRQ or data == COM_TIMEOUT_SPI:
            flag_number_errors = False
            flag_rave_error = False
            flag_rave_expected = False
            flag_errors = False
            flag_epoch_num = False
            flag_irq_memory_addr = False
            flag_irq_memory_word = False

        if data == COM_STM_START:
            print_mes.info(data, "Start STM32")
            errors.events_inc(errors.STM)
            flag_number_errors = False
            flag_errors = False
            flag_epoch_num = False
            number_errors = 0
            count_errors = 0
            continue

        elif data == COM_BUFFER_FILL:
            print_mes.error(data, "Buffer STM32 fill")
            buffer_fill += 1
            continue

        elif data == COM_CONFIG_end:
            print_mes.info(data, "Configuration completed")
            flag_number_errors = False
            flag_errors = False
            flag_epoch_num = False
            number_errors = 0
            count_errors = 0
            continue

        elif data == COM_ALRM_TMR:
            print_mes.error(data, "ALARM TIMER worked")
            errors.irq_inc(errors.ALRM_TMR)
            continue

        elif data == COM_ERR2_MEM:
            print_mes.error(data, "Flag ERR2_MEM worked")
            errors.irq_inc(errors.ERR2_MEM)
            continue

        elif data == COM_err_CORR_IRQ:
            print_mes.error(data, "err_CORR_IRQ interrupt occurred")
            errors.irq_inc(errors.ERR_CORR)
            continue

        elif data == COM_TMR1_IRQ:
            print_mes.error(data, "TMR1 interrupt occurred")
            errors.irq_inc(errors.TMR1)
            continue

        elif data == COM_TIMEOUT_SPI:
            print_mes.error(data, "SPI not good")
            errors.events_inc(errors.TIMEOUT_SPI)
            continue

        elif flag_rave_error is True:
            print_mes.error(data, "RAVE ERROR")
            flag_rave_error = False

        elif data == COM_RAVE:
            print_mes.error(data, "Invalid opcode came to stm32")
            errors.events_inc(errors.RAVE)
            flag_rave_expected = True
            continue

        elif flag_irq_memory_word is True:
            print_mes.error(data, "IRQ_MEMORY ERROR (word)")
            flag_irq_memory_word = False
            continue

        elif flag_irq_memory_addr is True:
            print_mes.error(data, "IRQ_MEMORY ERROR (address)")
            flag_irq_memory_addr = False
            flag_irq_memory_word = True
            continue

        elif flag_errors is True:
            print_mes.error(data, "ERRORS")
            count_errors += 1
            if count_errors >= number_errors * 2:
                flag_errors = False
                number_errors = 0
                count_errors = 0
            continue

        elif flag_number_errors is True:
            number_errors = int(data, 16)
            if number_errors == 0:
                print_mes.info(data, "Number ERRORS")
            elif number_errors > THRESHOLD_ERRORS:
                print_mes.error(data, "Number ERRORS")
                number_errors = THRESHOLD_ERRORS
                flag_errors = True
            else:
                print_mes.error(data, "Number ERRORS")
                flag_errors = True
            flag_number_errors = False
            errors.config_inc(int(data, 16))
            continue

        elif flag_rave_expected is True:
            print_mes.error(data, "RAVE Expected")
            flag_rave_expected = False
            flag_rave_error = True
            continue

        elif flag_epoch_num is True:
            print_mes.info(data, "Number epoch")
            flag_epoch_num = False
            last_epoch = int(data, 16)
            continue

        elif data == COM_TMRS_RELOAD_start:
            print_mes.info(data, "Start time reload")
            continue
        elif data == COM_TMRS_RELOAD_end:
            print_mes.info(data, "End time reload")
            continue

        elif data == COM_MEM0_READ_start:
            print_mes.info(data, "Start reading pattern_0 from memory")
            flag_number_errors = True
            errors.config_flag_set(errors.MEMORY)
            continue
        elif data == COM_MEM0_READ_end:
            print_mes.info(data, "End reading pattern_0 from memory")
            continue

        elif data == COM_MEM1_READ_start:
            print_mes.info(data, "Start reading pattern_1 from memory")
            flag_number_errors = True
            errors.config_flag_set(errors.MEMORY)
            continue
        elif data == COM_MEM1_READ_end:
            print_mes.info(data, "End reading pattern_1 from memory")
            continue

        elif data == COM_MEM0_WRITE_start:
            print_mes.info(data, "Start of writing pattern_0 in memory")
            continue
        elif data == COM_MEM0_WRITE_end:
            print_mes.info(data, "End of writing pattern_0 in memory")
            continue

        elif data == COM_MEM1_WRITE_start:
            print_mes.info(data, "Start of writing pattern_1 in memory")
            continue
        elif data == COM_MEM1_WRITE_end:
            print_mes.info(data, "End of writing pattern_1 in memory")
            continue

        elif data == COM_UART1_TRAN_CHECK_ok:
            print_mes.info(data, "UART1 transaction is successful")
            continue
        elif data == COM_UART1_TRAN_CHECK_error:
            print_mes.info(data, "UART1 transaction failed")
            flag_errors = True
            errors.tran_inc(errors.UART1)
            continue

        elif data == COM_UART2_TRAN_CHECK_ok:
            print_mes.info(data, "UART2 transaction is successful")
            continue
        elif data == COM_UART2_TRAN_CHECK_error:
            print_mes.info(data, "UART2 transaction failed")
            flag_errors = True
            errors.tran_inc(errors.UART2)
            continue

        elif data == COM_CHANNELS_READ_start:
            print_mes.info(data, "Start reading channels")
            flag_number_errors = True
            errors.config_flag_set(errors.CHANNELS)
            continue
        elif data == COM_CHANNELS_READ_end:
            print_mes.info(data, "End reading channels")
            continue

        elif data == COM_FTS_READ_start:
            print_mes.info(data, "Start reading FTS")
            flag_number_errors = True
            errors.config_flag_set(errors.FTS)
            continue
        elif data == COM_FTS_READ_end:
            print_mes.info(data, "End reading FTS")
            continue

        elif data == COM_TLM_READ_start:
            print_mes.info(data, "Start reading TLM")
            flag_number_errors = True
            errors.config_flag_set(errors.TLM)
            continue
        elif data == COM_TLM_READ_end:
            print_mes.info(data, "End reading TLM")
            continue

        elif data == COM_UART1_CONF_CHECK_start:
            print_mes.info(data, "Start UART1 configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.UART1)
            continue
        elif data == COM_UART1_CONF_CHECK_end:
            print_mes.info(data, "End UART1 configuration check")
            continue

        elif data == COM_UART2_CONF_CHECK_start:
            print_mes.info(data, "Start UART2 configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.UART2)
            continue
        elif data == COM_UART2_CONF_CHECK_end:
            print_mes.info(data, "End UART2 configuration check")
            continue

        elif data == COM_GPIO_CONF_CHECK_start:
            print_mes.info(data, "Start GPIO configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.GPIO)
            continue
        elif data == COM_GPIO_CONF_CHECK_end:
            print_mes.info(data, "End GPIO configuration check")
            continue

        elif data == COM_PLL_CONF_CHECK_start:
            print_mes.info(data, "Start PLL configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.PLL)
            continue
        elif data == COM_PLL_CONF_CHECK_end:
            print_mes.info(data, "End PLL configuration check")
            continue

        elif data == COM_TMR1_CONF_CHECK_start:
            print_mes.info(data, "Start TMR1 configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.TMR1)
            continue
        elif data == COM_TMR1_CONF_CHECK_end:
            print_mes.info(data, "End TMR1 configuration check")
            continue

        elif data == COM_ALRMTMR_CONF_CHECK_start:
            print_mes.info(data, "Start ALARM_TMR configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.ALRM_TMR)
            continue
        elif data == COM_ALRMTMR_CONF_CHECK_end:
            print_mes.info(data, "End ALARM_TMR configuration check")
            continue

        elif data == COM_SPI_CONF_CHECK_start:
            print_mes.info(data, "Start SPI configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.SPI)
            continue
        elif data == COM_SPI_CONF_CHECK_end:
            print_mes.info(data, "End SPI configuration check")
            continue

        elif data == COM_INMUX_CONF_CHECK_start:
            print_mes.info(data, "Start INMUX configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.INMUX)
            continue
        elif data == COM_INMUX_CONF_CHECK_end:
            print_mes.info(data, "End INMUX configuration check")
            continue

        elif data == COM_TSM_CONF_CHECK_start:
            print_mes.info(data, "Start TSM configuration check")
            flag_number_errors = True
            errors.config_flag_set(errors.TSM)
            continue
        elif data == COM_TSM_CONF_CHECK_end:
            print_mes.info(data, "End TSM configuration check")
            continue

        elif data == COM_STAGE_0_start:
            print_mes.info(data, "Start STAGE MEMORY_0")
            continue
        elif data == COM_STAGE_0_end:
            print_mes.info(data, "End STAGE MEMORY_0")
            continue

        elif data == COM_STAGE_1_start:
            print_mes.info(data, "Start STAGE MEMORY_1")
            continue
        elif data == COM_STAGE_1_end:
            print_mes.info(data, "End STAGE MEMORY_1")
            continue

        elif data == COM_STAGE_2_start:
            print_mes.info(data, "Start STAGE CONFIGURATION")
            continue
        elif data == COM_STAGE_2_end:
            print_mes.info(data, "End STAGE CONFIGURATION")
            continue

        # elif data == COM_TMR1_IRQ_start:
        #     print_mes.error(data, "Start INTERRUPT TMR1")
        #     errors.irq_inc(errors.TMR1)
        # elif data == COM_TMR1_IRQ_end:
        #     print_mes.error(data, "End INTERRUPT TMR1")

        elif data == COM_MEM_IRQ_start:
            print_mes.error(data, "Start INTERRUPT MEMORY")
            errors.irq_inc(errors.MEMORY)
            flag_irq_memory_addr = True
            continue
        elif data == COM_MEM_IRQ_end:
            print_mes.error(data, "End INTERRUPT MEMORY")
            continue

        elif data == COM_UNRESET_DEVICE:
            print_mes.info(data, "Unreset Cxemai6")
            errors.events_inc(errors.UNRESET_DEVICE)
            continue

        elif data == COM_OK:
            print_mes.info(data, "All OK")
            errors.events_inc(errors.OK)
            flag_epoch_num = True
            continue

        elif data == COM_MACHINE:
            print_mes.error(data, "Unexpected machine state failure stm32")
            errors.events_inc(errors.MACHINE)
            continue

        elif data == COM_FLAG_ERROR:
            print_mes.info(data, "Start of error frame")
            flag_epoch_num = True
            errors.events_inc(errors.FRAMES)
            continue

        elif data == "":
            print_mes.error(data, "Timeout UART")
            timeout_uart += 1
            continue

        else:
            print_mes.error(data, "Invalid OPCODE")
            invalid_opcode += 1
            continue

finally:
    curses.endwin()
