
PMD_NOERROR = 0
PMD_ERROR_RESET = 0X01
PMD_ERROR_INVALIDINSTRUCTION = 0X02
PMD_ERROR_INVALIDAXIS = 0X03
PMD_ERROR_INVALIDPARAMETER = 0X04
PMD_ERROR_TRACERUNNING = 0X05
PMD_ERROR_BLOCKOUTOFBOUNDS = 0X07
PMD_ERROR_TRACEBUFFERZERO = 0X08
PMD_ERROR_BADSERIALCHECKSUM = 0X09
PMD_ERROR_INVALIDNEGATIVEVALUE = 0X0B
PMD_ERROR_INVALIDPARAMETERCHANGE = 0X0C
PMD_ERROR_LIMITEVENTPENDING = 0X0D
PMD_ERROR_INVALIDMOVEINTOLIMIT = 0X0E
PMD_ERROR_INVALIDOPERATINGMODERESTORE = 0X10
PMD_ERROR_INVALIDOPERATINGMODEFORCOMMAND = 0X11
PMD_ERROR_BADSTATE = 0X12
PMD_ERROR_ATLASNOTDETECTED = 0X14
PMD_ERROR_HARDFAULT = 0X13
PMD_ERROR_BADSPICHECKSUM = 0X15
PMD_ERROR_INVALIDSPIPROTOCOL = 0X16
PMD_ERROR_INVALIDTORQUECOMMAND = 0X18
PMD_ERROR_BADFLASHCHECKSUM = 0X19
PMD_ERROR_INVALIDFLASHMODECOMMAND = 0X1A
PMD_ERROR_READONLY = 0X1B
PMD_ERROR_INITIALIZATIONONLYCOMMAND = 0X1C

errorMessage = {
    PMD_NOERROR:                              "No error",
    PMD_ERROR_RESET:                          "Processor reset",
    PMD_ERROR_INVALIDINSTRUCTION:             "Invalid instruction",
    PMD_ERROR_INVALIDAXIS:                    "Invalid axis",
    PMD_ERROR_INVALIDPARAMETER:               "Invalid data parameter",
    PMD_ERROR_TRACERUNNING:                   "Trace currently running",
    PMD_ERROR_BLOCKOUTOFBOUNDS:               "Block out of bounds",
    PMD_ERROR_TRACEBUFFERZERO:                "Zero length trace buffer",
    PMD_ERROR_BADSERIALCHECKSUM:              "Invalid checksum",
    PMD_ERROR_INVALIDNEGATIVEVALUE:           "Invalid negative value for profile mode",
    PMD_ERROR_INVALIDPARAMETERCHANGE:         "Invalid parameter change for profile mode",
    PMD_ERROR_LIMITEVENTPENDING:              "Invalid move with limit event pending",
    PMD_ERROR_INVALIDMOVEINTOLIMIT:           "Invalid move into limit",
    PMD_ERROR_INVALIDOPERATINGMODERESTORE:    "Invalid operating mode restore",
    PMD_ERROR_INVALIDOPERATINGMODEFORCOMMAND: "Command not valid in this operating mode",
    PMD_ERROR_BADSTATE:                       "Command not accepted in current state",
    PMD_ERROR_ATLASNOTDETECTED:               "Atlas command specified but no Atlas detected",
    PMD_ERROR_HARDFAULT:                      "A hard fault has occurred. The processor must be reset",
    PMD_ERROR_BADSPICHECKSUM:                 "Bad SPI command checksum",
    PMD_ERROR_INVALIDSPIPROTOCOL:             "Incorrect SPI command protocol",
    PMD_ERROR_INVALIDTORQUECOMMAND:           "Invalid torque command",
    PMD_ERROR_BADFLASHCHECKSUM:               "Bad flash checksum",
    PMD_ERROR_INVALIDFLASHMODECOMMAND:        "Command not valid in flash mode",
    PMD_ERROR_READONLY:                       "Write to read only buffer",
    PMD_ERROR_INITIALIZATIONONLYCOMMAND:      "Command valid only for initialization"
}


def GetErrorMessage(code: int) -> str:
    return errorMessage.get(code, "Unknown error")
