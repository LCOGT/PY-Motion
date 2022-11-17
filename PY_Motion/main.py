import inspect
import serial
import threading
import time
from typing import Tuple
from .commands import *
from .pmd_types import *

PYMOTION_MAJOR_VERSION = 5
PYMOTION_MINOR_VERSION = 0


class PMDCommunicationError(Exception):
    pass


class PMDAxisInterface:
    def __init__(self):
        self._mc = None  # motion controller
        self.lock = threading.Lock()

    def _write_command_with_arguments(self, command: bytearray) -> None:
        command[1] = 0
        command[1] = ((sum(command) ^ 0xFF) + 1) & 0xFF
        self._mc.write(command)

    def _read_response(self, length: int) -> bytes:
        response = self._mc.read(length)
        if len(response) < 2:
            raise PMDCommunicationError('timeout waiting for motion controller to respond')
        if (sum(response) & 0xFF) != 0:
            raise PMDCommunicationError('transmission error detected in motion controller response')
        if response[0] != 0:
            caller = inspect.currentframe().f_back.f_code.co_name
            raise PMDCommandError(caller, response[0])
        return response

    def SetupAxisInterface_Serial(self, port: str, baudrate: int) -> None:
        self._mc = serial.Serial(port, baudrate, timeout=0.001)
        zero = bytes([0x00])
        response = bytearray()
        synch_attempts = 100
        while len(response) == 0 and synch_attempts > 0:
            self._mc.write(zero)
            response = self._mc.read(2)
            synch_attempts -= 1
        if synch_attempts == 0:
            raise PMDCommunicationError('Unable to communicate with motion processor')
        self._mc.timeout = 0.1

    def CloseAxisInterface(self) -> None:
        self._mc.close()
        self._mc = None
        self.lock = None

    @staticmethod
    def GetPYMotionVersion() -> Tuple[int, int]:
        return PYMOTION_MAJOR_VERSION, PYMOTION_MINOR_VERSION

    def GetVersion(self) -> PMDVersion:
        self._mc.write(PMD_COMMAND_GETVERSION)
        response = self._read_response(6)
        return PMDVersion(response[2:6])

    def NoOperation(self) -> None:
        self._mc.write(PMD_COMMAND_NOOPERATION)
        self._read_response(2)

    def GetInstructionError(self) -> int:
        self._mc.write(PMD_COMMAND_GETINSTRUCTIONERROR)
        response = self._read_response(4)
        return int.from_bytes(response[2:4], byteorder='big')

    def Reset(self) -> None:
        self._mc.write(PMD_COMMAND_RESET)
        self._read_response(2)
        time.sleep(0.4)  # wait 400ms for chip to reset

        # After the reset, the chip's InstructionError register should contain PMD_ERROR_RESET.
        # Calling GetInstructionError will reset the register to PMD_ERROR_NONE
        error_code = self.GetInstructionError()
        if error_code != PMD_ERROR_RESET:
            raise PMDCommandError("Reset", error_code)

    def GetSampleTime(self) -> int:
        self._mc.write(PMD_COMMAND_GETSAMPLETIME)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big')

    def GetEncoderSource(self, axis: PMDAxis) -> PMDEncoderSource:
        command = PMD_COMMAND_GETENCODERSOURCE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDEncoderSource(response[3])

    def SetEncoderSource(self, axis: PMDAxis, source: PMDEncoderSource) -> None:
        command = PMD_COMMAND_SETENCODERSOURCE
        command[2] = axis.value
        command[5] = source.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetEncoderToStepRatio(self, axis: PMDAxis) -> Tuple[int, int]:
        command = PMD_COMMAND_GETENCODERTOSTEPRATIO
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        counts = int.from_bytes(response[2:4], byteorder='big')
        steps = int.from_bytes(response[4:6], byteorder='big')
        return counts, steps

    def SetEncoderToStepRatio(self, axis: PMDAxis, counts: int, steps: int) -> None:
        command = PMD_COMMAND_SETENCODERTOSTEPRATIO
        command[2] = axis.value
        command[4:6] = counts.to_bytes(2, byteorder='big')
        command[6:8] = steps.to_bytes(2, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetActualPositionUnits(self, axis: PMDAxis) -> PMDPositionUnits:
        command = PMD_COMMAND_GETACTUALPOSITIONUNITS
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDPositionUnits(response[3])

    def SetActualPositionUnits(self, axis: PMDAxis, units: PMDPositionUnits) -> None:
        command = PMD_COMMAND_SETACTUALPOSITIONUNITS
        command[2] = axis.value
        command[5] = units.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetSignalSense(self, axis: PMDAxis) -> PMDSignalSense:
        command = PMD_COMMAND_GETSIGNALSENSE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDSignalSense(int.from_bytes(response[2:4], byteorder='big'))

    def SetSignalSense(self, axis: PMDAxis, sense: PMDSignalSense) -> None:
        command = PMD_COMMAND_SETSIGNALSENSE
        command[2] = axis.value
        command[4:6] = sense.value.to_bytes(2, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetPositionErrorLimit(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETPOSITIONERRORLIMIT
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big')

    def SetPositionErrorLimit(self, axis: PMDAxis, limit: int) -> None:
        command = PMD_COMMAND_SETPOSITIONERRORLIMIT
        command[2] = axis.value
        command[4:8] = limit.to_bytes(4, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetEventAction(self, axis: PMDAxis, event: PMDEvent) -> PMDAction:
        command = PMD_COMMAND_GETEVENTACTION
        command[2] = axis.value
        command[5] = event.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDAction(int.from_bytes(response[2:4], byteorder='big'))

    def SetEventAction(self, axis: PMDAxis, event: PMDEvent, action: PMDAction) -> None:
        command = PMD_COMMAND_SETEVENTACTION
        command[2] = axis.value
        command[5] = event.value
        command[7] = action.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetProfileMode(self, axis: PMDAxis) -> PMDProfileMode:
        command = PMD_COMMAND_GETPROFILEMODE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDProfileMode(response[3])

    def SetProfileMode(self, axis: PMDAxis, mode: PMDProfileMode) -> None:
        command = PMD_COMMAND_SETPROFILEMODE
        command[2] = axis.value
        command[5] = mode.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetCaptureSource(self, axis: PMDAxis) -> PMDCaptureSource:
        command = PMD_COMMAND_GETCAPTURESOURCE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDCaptureSource(response[3])

    def SetCaptureSource(self, axis: PMDAxis, source: PMDCaptureSource) -> None:
        command = PMD_COMMAND_SETCAPTURESOURCE
        command[2] = axis.value
        command[5] = source.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetStopMode(self, axis: PMDAxis) -> PMDStopMode:
        command = PMD_COMMAND_GETSTOPMODE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDStopMode(response[3])

    def SetStopMode(self, axis: PMDAxis, mode: PMDStopMode) -> None:
        command = PMD_COMMAND_SETSTOPMODE
        command[2] = axis.value
        command[5] = mode.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetBreakpoint(self, axis: PMDAxis, breakpt: PMDBreakpoint) -> Tuple[PMDAxis, PMDAction, PMDTrigger]:
        command = PMD_COMMAND_GETBREAKPOINT
        command[2] = axis.value
        command[5] = breakpt.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        source = PMDAxis(response[3] & 0x0F)
        action = PMDAction(response[3] >> 4)
        trigger = PMDTrigger(response[2])
        return source, action, trigger

    def SetBreakpoint(
        self, axis: PMDAxis, breakpt: PMDBreakpoint, source: PMDAxis, action: PMDAction, trigger: PMDTrigger
    ) -> None:
        command = PMD_COMMAND_SETBREAKPOINT
        command[2] = axis.value
        command[5] = breakpt.value
        command[6] = trigger.value
        command[7] = action.value << 4 | source.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetBreakpointValue(self, axis: PMDAxis, breakpt: PMDBreakpoint) -> int:
        command = PMD_COMMAND_GETBREAKPOINTVALUE
        command[2] = axis.value
        command[5] = breakpt.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big')

    def SetBreakpointValue(self, axis: PMDAxis, breakpt: PMDBreakpoint, value: int) -> None:
        command = PMD_COMMAND_SETBREAKPOINTVALUE
        command[2] = axis.value
        command[5] = breakpt.value
        command[6:10] = value.to_bytes(4, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetVelocity(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETVELOCITY
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big', signed=True)

    def SetVelocity(self, axis: PMDAxis, velocity: int) -> None:
        command = PMD_COMMAND_SETVELOCITY
        command[2] = axis.value
        command[4:8] = velocity.to_bytes(4, byteorder='big', signed=True)
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetAcceleration(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETACCELERATION
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big')

    def SetAcceleration(self, axis: PMDAxis, acceleration: int) -> None:
        command = PMD_COMMAND_SETACCELERATION
        command[2] = axis.value
        command[4:8] = acceleration.to_bytes(4, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetJerk(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETJERK
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big')

    def SetJerk(self, axis: PMDAxis, jerk: int) -> None:
        command = PMD_COMMAND_SETJERK
        command[2] = axis.value
        command[4:8] = jerk.to_bytes(4, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetActualPosition(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETACTUALPOSITION
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big', signed=True)

    def AdjustActualPosition(self, axis: PMDAxis, position: int) -> None:
        command = PMD_COMMAND_ADJUSTACTUALPOSITION
        command[2] = axis.value
        command[4:8] = position.to_bytes(4, byteorder='big', signed=True)
        self._write_command_with_arguments(command)
        self._read_response(2)

    def SetActualPosition(self, axis: PMDAxis, position: int) -> None:
        command = PMD_COMMAND_SETACTUALPOSITION
        command[2] = axis.value
        command[4:8] = position.to_bytes(4, byteorder='big', signed=True)
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetPosition(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETPOSITION
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big', signed=True)

    def SetPosition(self, axis: PMDAxis, position: int) -> None:
        command = PMD_COMMAND_SETPOSITION
        command[2] = axis.value
        command[4:8] = position.to_bytes(4, byteorder='big', signed=True)
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetPositionError(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETPOSITIONERROR
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big', signed=True)

    def ClearPositionError(self, axis: PMDAxis) -> None:
        command = PMD_COMMAND_CLEARPOSITIONERROR
        command[2] = axis.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def Update(self, axis: PMDAxis) -> None:
        command = PMD_COMMAND_UPDATE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def MultiUpdate(self, axes: PMDAxisMask) -> None:
        command = PMD_COMMAND_MULTIUPDATE
        command[5] = axes.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetActivityStatus(self, axis: PMDAxis) -> PMDActivityStatus:
        command = PMD_COMMAND_GETACTIVITYSTATUS
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDActivityStatus(response[2:4])

    def GetSignalStatus(self, axis: PMDAxis) -> PMDSignalStatus:
        command = PMD_COMMAND_GETSIGNALSTATUS
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDSignalStatus(int.from_bytes(response[2:4], byteorder='big'))

    def GetEventStatus(self, axis: PMDAxis) -> PMDEventStatus:
        command = PMD_COMMAND_GETEVENTSTATUS
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDEventStatus(int.from_bytes(response[2:4], byteorder='big'))

    def ResetEventStatus(self, axis: PMDAxis, mask: PMDEventStatus) -> None:
        command = PMD_COMMAND_RESETEVENTSTATUS
        command[2] = axis.value
        command[4:6] = mask.value.to_bytes(2, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)

    def GetCaptureValue(self, axis: PMDAxis) -> int:
        command = PMD_COMMAND_GETCAPTUREVALUE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(6)
        return int.from_bytes(response[2:6], byteorder='big', signed=True)

    def GetOperatingMode(self, axis: PMDAxis) -> PMDOperatingMode:
        command = PMD_COMMAND_GETOPERATINGMODE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return PMDOperatingMode(response[3])

    def SetOperatingMode(self, axis: PMDAxis, mode: PMDOperatingMode) -> None:
        command = PMD_COMMAND_SETOPERATINGMODE
        command[2] = axis.value
        command[5] = mode.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def RestoreOperatingMode(self, axis: PMDAxis) -> None:
        command = PMD_COMMAND_RESTOREOPERATINGMODE
        command[2] = axis.value
        self._write_command_with_arguments(command)
        self._read_response(2)

    def ReadIO(self, address: int) -> int:
        command = PMD_COMMAND_READIO
        command[5] = address
        self._write_command_with_arguments(command)
        response = self._read_response(4)
        return int.from_bytes(response[2:4], byteorder='big')

    def WriteIO(self, address: int, data: int) -> None:
        command = PMD_COMMAND_WRITEIO
        command[5] = address
        command[6:8] = int.to_bytes(data, 2, byteorder='big')
        self._write_command_with_arguments(command)
        self._read_response(2)
