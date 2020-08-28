class CountErrors:
    MEMORY = "Memory"
    CHANNELS = "Channels"
    FTS = "FTS"
    TLM = "TLM"
    UART1 = "UART1"
    UART2 = "UART2"
    GPIO = "GPIO"
    PLL = "PLL"
    TMR1 = "TMR1"
    ALRM_TMR = "ALRM_TMR"
    SPI = "SPI"
    INMUX = "INMUX"
    TSM = "TSM"

    ERR2_MEM = "ERR2_MEM"
    ERR_CORR = "err_CORR"

    STM = "STM Start"
    UNRESET_DEVICE = "Unreset Cxemai6"
    TIMEOUT_SPI = "Timeout SPI"
    RAVE = "RAVE"
    MACHINE = "MACHINE"
    FRAMES = "Errors Frames"
    OK = "OK"

    errors_count_config = {"Memory": 0,
                           "Channels": 0,
                           "FTS": 0,
                           "TLM": 0,
                           "UART1": 0,
                           "UART2": 0,
                           "GPIO": 0,
                           "PLL": 0,
                           "TMR1": 0,
                           "ALRM_TMR": 0,
                           "SPI": 0,
                           "INMUX": 0,
                           "TSM": 0}

    errors_flags_config = {"Memory": False,
                           "Channels": False,
                           "FTS": False,
                           "TLM": False,
                           "UART1": False,
                           "UART2": False,
                           "GPIO": False,
                           "PLL": False,
                           "TMR1": False,
                           "ALRM_TMR": False,
                           "SPI": False,
                           "INMUX": False,
                           "TSM": False}

    tran_count = {"UART1": 0,
                  "UART2": 0}

    irq_count = {"ALRM_TMR": 0,
                 "ERR2_MEM": 0,
                 "err_CORR": 0,
                 "TMR1": 0,
                 "Memory": 0}

    event_count = {"STM Start": 0,
                   "Unreset Cxemai6": 0,
                   "Timeout SPI": 0,
                   "RAVE": 0,
                   "MACHINE": 0,
                   "Errors Frames": 0,
                   "OK": 0}

    def config_flag_set(self, item):
        self.errors_flags_config[item] = True

    def config_inc(self, number):
        for key, value in self.errors_flags_config.items():
            if value is True:
                self.errors_count_config[key] += number
                self.errors_flags_config[key] = False

    def tran_inc(self, item):
        self.tran_count[item] += 1

    def irq_inc(self, item):
        self.irq_count[item] += 1

    def events_inc(self, item):
        self.event_count[item] += 1
