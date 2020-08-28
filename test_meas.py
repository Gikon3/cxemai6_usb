meas_irq_count = 0
flag_mem_0 = 0
flag_mem_1 = 0
flag_channels = 0

for i in range(100):
    flag_mem_0 = 0
    flag_mem_1 = 0
    flag_channels = 0

    meas_irq_count += 1

    if ((meas_irq_count - 1) % 20 == 0) and (meas_irq_count != 1):
        if meas_irq_count == 21:
            flag_mem_0 = 1
        elif meas_irq_count == 1021:
            flag_mem_1 = 1
        else:
            flag_channels = 1

    if meas_irq_count == 2001:
        meas_irq_count = 1

    print(i, flag_mem_0, flag_channels, flag_mem_1)
