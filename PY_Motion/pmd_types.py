from enum import Enum, Flag


class PMDAction(Enum):
    NONE = 0
    ABRUPT_STOP = 2
    SMOOTH_STOP = 3
    DISABLE_POSITION_LOOP = 5
    DISABLE_CURRENT_LOOP = 6
    DISABLE_MOTOR_OUTPUT = 7
    ABRUPT_STOP_POSITION_ERROR_CLEAR = 8


class PMDActivityStatus:
    def __init__(self, status: bytes):
        self._status = status

    @property
    def at_max_velocity(self):
        return self._status[1] & 0x02 != 0

    @property
    def tracking(self):
        return self._status[1] & 0x04 != 0

    @property
    def profile_mode(self):
        return (self._status[1] >> 3) & 0x07

    @property
    def axis_settled(self):
        return self._status[1] & 0x80 != 0

    @property
    def motor_on(self):
        return self._status[0] & 0x01 != 0

    @property
    def position_capture(self):
        return self._status[0] & 0x02 != 0

    @property
    def in_motion(self):
        return self._status[0] & 0x04 != 0

    @property
    def in_positive_limit(self):
        return self._status[0] & 0x08 != 0

    @property
    def in_negative_limit(self):
        return self._status[0] & 0x10 != 0

    @property
    def profile_segment(self):
        return self._status[0] >> 5 & 0x07

    @property
    def value(self):
        return int.from_bytes(self._status, byteorder='big')


class PMDAxis(Enum):
    AXIS1 = 0
    AXIS2 = 1
    AXIS3 = 2
    AXIS4 = 3


# convenience aliases for PMDAxis enums
AXIS1 = PMDAxis.AXIS1
AXIS2 = PMDAxis.AXIS2
AXIS3 = PMDAxis.AXIS3
AXIS4 = PMDAxis.AXIS4


class PMDAxisMask(Flag):
    AXIS1 = 1
    AXIS2 = 2
    AXIS3 = 4
    AXIS4 = 8


class PMDBreakpoint(Enum):
    BREAKPOINT1 = 0
    BREAKPOINT2 = 1


class PMDCaptureSource(Enum):
    INDEX = 0
    HOME = 1
    HIGH_SPEED_CAPTURE = 2


class PMDEncoderSource(Enum):
    INCREMENTAL = 0
    PARALLEL = 1
    NONE = 2
    LOOPBACK = 3
    PULSE_AND_DIRECTION = 4
    RESERVED = 5
    PARALLEL_32BIT = 6


class PMDEvent(Enum):
    IMMEDIATE = 0
    POSITIVE_LIMIT = 1
    NEGATIVE_LIMIT = 2
    MOTION_ERROR = 3
    CURRENT_FOLDBACK = 4


class PMDEventStatus(Flag):
    NONE = 0x0000
    MOTION_COMPLETE = 0x0001
    WRAP_AROUND = 0x0002
    BREAKPOINT1 = 0x0004
    CAPTURE_RECEIVED = 0x0008
    MOTION_ERROR = 0x0010
    POSITIVE_LIMIT = 0x0020
    NEGATIVE_LIMIT = 0x0040
    INSTRUCTION_ERROR = 0x0080
    DRIVE_DISABLED = 0x0100
    OVERTEMPERATURE = 0x0200
    DRIVE_EXCEPTION = 0x0400
    COMMUTATION_ERROR = 0x800
    CURRENT_FOLDBACK = 0x1000
    BREAKPOINT2 = 0x2000


class PMDMotorType(Enum):
    SERVO = 1
    BRUSHLESS = 3
    MICROSTEPPING = 4
    PULSE_AND_DIRECTION = 5
    ALL_MOTOR_TYPES = 8
    ION_ANY_MOTOR_TYPE = 9


class PMDPositionUnits(Enum):
    COUNTS = 0
    STEPS = 1


class PMDOperatingMode(Flag):
    AXIS_ENABLED = 0x0001
    MOTOR_OUTPUT_ENABLED = 0x0002
    CURRENT_CONTROL_ENABLED = 0x0004
    POSITION_LOOP_ENABLED = 0x0010
    TRAJECTORY_ENABLED = 0x0020


class PMDProductFamily(Enum):
    NAVIGATOR = 2
    PILOT = 3
    MAGELLAN = 5
    ION = 9


class PMDProfileMode(Enum):
    TRAPEZOIDAL = 0
    VELOCITY_CONTOURING = 1
    S_CURVE = 2
    ELECTRONIC_GEAR = 3


class PMDSignalSense(Flag):
    DEFAULT = 0x0000
    ENCODER_A = 0x0001
    ENCODER_B = 0x0002
    ENCODER_INDEX = 0x0004
    HOME = 0x0008
    POSITIVE_LIMIT = 0x0010
    NEGATIVE_LIMIT = 0x0020
    AXIS_IN = 0x0040
    HALL_A = 0x0080
    HALL_B = 0x0100
    HALL_C = 0x0200
    AXIS_OUT = 0x0400
    STEP_OUTPUT = 0x0800
    MOTOR_DIRECTION = 0x1000


class PMDSignalStatus(Flag):
    NONE = 0x0000
    ENCODER_A = 0x0001
    ENCODER_B = 0x0002
    ENCODER_INDEX = 0x0004
    HOME = 0x0008
    POSITIVE_LIMIT = 0x0010
    NEGATIVE_LIMIT = 0x0020
    AXIS_IN = 0x0040
    HALL_A = 0x0080
    HALL_B = 0x0100
    HALL_C = 0x0200
    AXIS_OUT = 0x0400
    RESERVED = 0x0800
    RESERVED2 = 0x1000
    ENABLE_IN = 0x2000
    FAULT_OUT = 0x4000


class PMDStopMode(Enum):
    NO_STOP = 0
    ABRUPT_STOP = 1
    SMOOTH_STOP = 2


class PMDTrigger(Enum):
    NONE = 0
    GT_OR_EQ_COMMANDED_POSITION = 1
    LT_OR_EQ_COMMANDED_POSITION = 2
    GT_OR_EQ_ACTUAL_POSITION = 3
    LT_OR_EQ_ACTUAL_POSITION = 4
    COMMANDED_POSITION_CROSSED = 5
    ACTUAL_POSITION_CROSSED = 6
    TIME = 7
    EVENT_STATUS = 8
    ACTIVITY_STATUS = 9
    SIGNAL_STATUS = 10
    DRIVE_STATUS = 11


class PMDVersion:
    def __init__(self, version: bytes):
        self._version = version

    @property
    def family(self):
        return PMDProductFamily(self._version[0] >> 4)

    @property
    def motor_type(self):
        return PMDMotorType(self._version[0] & 0x0F)

    @property
    def number_of_axes(self):
        return self._version[1] >> 4

    @property
    def chip_count(self):
        return self._version[1] & 0x03

    @property
    def custom(self):
        return self._version[2]

    @property
    def major(self):
        return self._version[3] >> 4

    @property
    def minor(self):
        return self._version[3] & 0x0F
