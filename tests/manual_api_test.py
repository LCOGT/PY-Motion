import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PY_Motion.main import *

if __name__ == '__main__':
    pmd = PMDAxisInterface()
    major, minor = pmd.GetPYMotionVersion()
    print(f'PY-Motion version {major}.{minor}\n')

    pmd.SetupAxisInterface_Serial('/dev/ttyAMA0', 115200)

    version = pmd.GetVersion()
    print(f'Product family = {version.family}')
    print(f'Motor type = {version.motor_type}')
    print(f'Number of axes = {version.number_of_axes}')
    print(f'Number of chips = {version.chip_count}')
    print(f'Customization code = {version.custom}')
    print(f'Firmware version = {version.major}.{version.minor}\n')

    print('testing NoOperation()...', end='', flush=True)
    for i in range(3):
        pmd.NoOperation()
    print('passed')

    print('testing Reset()...', end='', flush=True)
    pmd.Reset()
    print('passed')

    print('testing GetInstructionError()...', end='', flush=True)
    expected = 0
    received = pmd.GetInstructionError()
    assert(received == expected), f'GetInstructionError() expected {expected}, received {received}'
    print('passed')

    print('testing GetSampleTime()...', end='', flush=True)
    sample_time = pmd.GetSampleTime()
    print('passed')
    print(f'Sample time is {sample_time}us')

    print('testing Get/SetEncoderSource()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDEncoderSource.LOOPBACK
        received = pmd.GetEncoderSource(axis)
        assert(received == expected), f'GetEncoderSource() expected {expected}, received {received}'
        expected = PMDEncoderSource.INCREMENTAL
        pmd.SetEncoderSource(axis, expected)
        received = pmd.GetEncoderSource(axis)
        assert(received == expected), f'GetEncoderSource() expected {expected}, received {received}'
        pmd.SetEncoderSource(axis, PMDEncoderSource.LOOPBACK)
    print('passed')

    print('testing Get/SetEncoderToStepRatio()...', end='', flush=True)
    for axis in PMDAxis:
        expected = (1, 1)
        received = pmd.GetEncoderToStepRatio(axis)
        assert(received == expected), f'GetEncoderToStepRatio() expected {expected}, received {received}'
        expected = (256, 243)
        pmd.SetEncoderToStepRatio(axis, expected[0], expected[1])
        received = pmd.GetEncoderToStepRatio(axis)
        assert(received == expected), f'GetEncoderToStepRatio() expected {expected}, received {received}'
        pmd.SetEncoderToStepRatio(axis, 1, 1)
    print('passed')

    print('testing Get/SetActualPositionUnits()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDPositionUnits.STEPS
        received = pmd.GetActualPositionUnits(axis)
        assert(received == expected), f'GetActualPositionUnits() expected {expected}, received {received}'
        expected = PMDPositionUnits.COUNTS
        pmd.SetActualPositionUnits(axis, expected)
        received = pmd.GetActualPositionUnits(axis)
        assert(received == expected), f'GetActualPositionUnits() expected {expected}, received {received}'
        pmd.SetActualPositionUnits(axis, PMDPositionUnits.STEPS)
    print('passed')

    print('testing Get/SetSignalSense()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDSignalSense.STEP_OUTPUT
        received = pmd.GetSignalSense(axis)
        assert(received == expected), f'GetSignalSense() expected {expected}, received {received}'
        expected = PMDSignalSense(0x0830)
        pmd.SetSignalSense(axis, expected)
        received = pmd.GetSignalSense(axis)
        assert(received == expected), f'GetSignalSense() expected {expected}, received {received}'
        pmd.SetSignalSense(axis, PMDSignalSense.STEP_OUTPUT)
    print('passed')

    print('testing Get/SetPositionErrorLimit()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 65535
        received = pmd.GetPositionErrorLimit(axis)
        assert(received == expected), f'GetPositionErrorLimit() expected {expected}, received {received}'
        expected = 999
        pmd.SetPositionErrorLimit(axis, expected)
        received = pmd.GetPositionErrorLimit(axis)
        assert(received == expected), f'GetPositionErrorLimit() expected {expected}, received {received}'
        pmd.SetPositionErrorLimit(axis, 65535)
    print('passed')

    print('testing Get/SetEventAction()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDAction.ABRUPT_STOP_POSITION_ERROR_CLEAR
        received = pmd.GetEventAction(axis, PMDEvent.NEGATIVE_LIMIT)
        assert(received == expected), f'GetEventAction() expected {expected}, received {received}'
        expected = PMDAction.ABRUPT_STOP
        pmd.SetEventAction(axis, PMDEvent.NEGATIVE_LIMIT, expected)
        received = pmd.GetEventAction(axis, PMDEvent.NEGATIVE_LIMIT)
        assert(received == expected), f'GetEventAction() expected {expected}, received {received}'
        pmd.SetEventAction(axis, PMDEvent.NEGATIVE_LIMIT, PMDAction.ABRUPT_STOP_POSITION_ERROR_CLEAR)
    print('passed')

    print('testing Get/SetProfileMode()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDProfileMode.TRAPEZOIDAL
        received = pmd.GetProfileMode(axis)
        assert(received == expected), f'GetProfileMode() expected {expected}, received {received}'
        expected = PMDProfileMode.S_CURVE
        pmd.SetProfileMode(axis, expected)
        received = pmd.GetProfileMode(axis)
        assert(received == expected), f'GetProfileMode() expected {expected}, received {received}'
        pmd.SetProfileMode(axis, PMDProfileMode.TRAPEZOIDAL)
    print('passed')

    print('testing Get/SetCaptureSource()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDCaptureSource.INDEX
        received = pmd.GetCaptureSource(axis)
        assert(received == expected), f'GetCaptureSource() expected {expected}, received {received}'
        expected = PMDCaptureSource.HOME
        pmd.SetCaptureSource(axis, expected)
        received = pmd.GetCaptureSource(axis)
        assert(received == expected), f'GetCaptureSource() expected {expected}, received {received}'
        pmd.SetCaptureSource(axis, PMDCaptureSource.INDEX)
    print('passed')

    print('testing Get/SetStopMode()...', end='', flush=True)
    for axis in PMDAxis:
        expected = PMDStopMode.NO_STOP
        received = pmd.GetStopMode(axis)
        assert(received == expected), f'GetStopMode() expected {expected}, received {received}'
        expected = PMDStopMode.ABRUPT_STOP
        pmd.SetStopMode(axis, expected)
        received = pmd.GetStopMode(axis)
        assert(received == expected), f'GetStopMode() expected {expected}, received {received}'
        pmd.SetStopMode(axis, PMDStopMode.NO_STOP)
    print('passed')

    print('testing Get/SetBreakpoint()...', end='', flush=True)
    for axis in PMDAxis:
        for breakpt in PMDBreakpoint:
            expected = (AXIS1, PMDAction.NONE, PMDTrigger.NONE)
            received = pmd.GetBreakpoint(axis, breakpt)
            assert(received == expected), f'GetBreakpoint() expected {expected}, received {received}'
            expected = (axis, PMDAction.ABRUPT_STOP, PMDTrigger.SIGNAL_STATUS)
            pmd.SetBreakpoint(axis, breakpt, expected[0], expected[1], expected[2])
            received = pmd.GetBreakpoint(axis, breakpt)
            assert(received == expected), f'GetBreakpoint() expected {expected}, received {received}'
            pmd.SetBreakpoint(axis, breakpt, axis, PMDAction.NONE, PMDTrigger.NONE)
    print('passed')

    print('testing Get/SetBreakpointValue()...', end='', flush=True)
    for axis in PMDAxis:
        for breakpt in PMDBreakpoint:
            expected = 0
            received = pmd.GetBreakpointValue(axis, breakpt)
            assert(received == expected), f'GetBreakpointValue() expected {expected}, received {received}'
            expected = PMDSignalStatus.NEGATIVE_LIMIT.value << 16
            pmd.SetBreakpointValue(axis, breakpt, expected)
            received = pmd.GetBreakpointValue(axis, breakpt)
            assert(received == expected), f'GetBreakpointValue() expected {expected}, received {received}'
            pmd.SetBreakpointValue(axis, breakpt, 0)
    print('passed')

    print('testing Get/SetVelocity()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 0
        received = pmd.GetVelocity(axis)
        assert(received == expected), f'GetVelocity() expected {expected}, received {received}'
        expected = 11337
        pmd.SetVelocity(axis, expected)
        received = pmd.GetVelocity(axis)
        assert(received == expected), f'GetVelocity() expected {expected}, received {received}'
        pmd.SetVelocity(axis, 0)
    print('passed')

    print('testing Get/SetAcceleration()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 0
        received = pmd.GetAcceleration(axis)
        assert(received == expected), f'GetAcceleration() expected {expected}, received {received}'
        expected = 21337
        pmd.SetAcceleration(axis, expected)
        received = pmd.GetAcceleration(axis)
        assert(received == expected), f'GetAcceleration() expected {expected}, received {received}'
        pmd.SetAcceleration(axis, 0)
    print('passed')

    print('testing Get/SetJerk()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 0
        received = pmd.GetJerk(axis)
        assert(received == expected), f'GetJerk() expected {expected}, received {received}'
        expected = 31337
        pmd.SetJerk(axis, expected)
        received = pmd.GetJerk(axis)
        assert(received == expected), f'GetJerk() expected {expected}, received {received}'
        pmd.SetJerk(axis, 0)
    print('passed')

    print('testing Get/SetActualPosition()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 0
        received = pmd.GetActualPosition(axis)
        assert(received == expected), f'GetActualPosition() expected {expected}, received {received}'
        expected = 1234567
        pmd.SetActualPosition(axis, expected)
        received = pmd.GetActualPosition(axis)
        assert(received == expected), f'GetActualPosition() expected {expected}, received {received}'
        pmd.SetActualPosition(axis, 0)
    print('passed')

    print('testing AdjustActualPosition()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 10000
        pmd.AdjustActualPosition(axis, expected)
        received = pmd.GetActualPosition(axis)
        assert(received == expected), f'AdjustActualPosition() expected {expected}, received {received}'
        pmd.AdjustActualPosition(axis, -expected)
        received = pmd.GetActualPosition(axis)
        assert(received == 0), f'AdjustActualPosition() expected 0, received {received}'
    print('passed')

    print('testing Get/SetPosition()...', end='', flush=True)
    for axis in PMDAxis:
        expected = 0
        received = pmd.GetPosition(axis)
        assert(received == expected), f'GetPosition() expected {expected}, received {received}'
        expected = 10000
        pmd.SetPosition(axis, expected)
        received = pmd.GetPosition(axis)
        assert(received == expected), f'GetPosition() expected {expected}, received {received}'
        pmd.SetPosition(axis, 0)
    print('passed')

    print('testing Update()...', end='', flush=True)
    steps_per_second = 100.0
    velocity = int(round((steps_per_second * sample_time / 1000000.0) * 65536.0))
    for axis in PMDAxis:
        pmd.SetVelocity(axis, velocity)
        pmd.SetAcceleration(axis, velocity)
        expected = 100
        pmd.SetPosition(axis, expected)
        pmd.Update(axis)
        time.sleep(1.0)
        received = pmd.GetActualPosition(axis)
        assert(received == expected), f'GetActualPosition() expected {expected}, received {received}'
    print('passed')

    print('testing MultiUpdate()...', end='', flush=True)
    expected = 200
    for axis in PMDAxis:
        pmd.SetPosition(axis, expected)
    pmd.MultiUpdate(PMDAxisMask(0b1111))
    time.sleep(1.0)
    for axis in PMDAxis:
        received = pmd.GetActualPosition(axis)
        assert (received == expected), f'GetActualPosition() expected {expected}, received {received}'
    print('passed')

    print('testing GetActivityStatus()...', end='', flush=True)
    for axis in PMDAxis:
        pmd.SetPosition(axis, 300)
        pmd.Update(axis)
        status = pmd.GetActivityStatus(axis)
        assert status.in_motion, 'GetActivityStatus() expected in_motion==True, found False'
        start = time.time()
        while status.in_motion:
            assert (time.time() - start < 2.0), 'GetActivityStatus() expected in_motion==False, found True'
            status = pmd.GetActivityStatus(axis)
    print('passed')

    print('testing Get/ResetEventStatus()...', end='', flush=True)
    for axis in PMDAxis:
        pmd.ResetEventStatus(axis, PMDEventStatus(0))
        pmd.SetPosition(axis, 400)
        pmd.Update(axis)
        status = pmd.GetEventStatus(axis)
        assert not (status & PMDEventStatus.MOTION_COMPLETE),\
            'GetEventStatus() expected MOTION_COMPLETE==False, found True'
        start = time.time()
        while not (status & PMDEventStatus.MOTION_COMPLETE):
            assert(time.time() - start < 2.0), 'GetEventStatus() expected MOTION_COMPLETE==True, found False'
            status = pmd.GetEventStatus(axis)
        pmd.ResetEventStatus(axis, PMDEventStatus(0))
        status = pmd.GetEventStatus(axis)
        assert not (status & PMDEventStatus.MOTION_COMPLETE),\
            'GetEventStatus() expected MOTION_COMPLETE==False, found True'
    print('passed')

    print('testing GetSignalStatus()...', end='', flush=True)
    for axis in PMDAxis:
        received = pmd.GetSignalStatus(axis)
        pmd.SetSignalSense(axis, PMDSignalSense.STEP_OUTPUT | PMDSignalSense(0x03B0))
        expected = PMDSignalStatus(received.value ^ 0x03B0)
        received = pmd.GetSignalStatus(axis)
        assert (received == expected), f'GetSignalStatus({axis}) expected {expected}, received {received}'
        pmd.SetSignalSense(axis, PMDSignalSense.STEP_OUTPUT)
    print('passed')

    print('testing Get/ClearPositionError...', end='', flush=True)
    for axis in PMDAxis:
        expected = 0
        received = pmd.GetPositionError(axis)
        assert (received == expected), f'GetPositionError() expected {expected}, received {received}'
        pmd.SetEncoderSource(axis, PMDEncoderSource.INCREMENTAL)
        pmd.SetPosition(axis, 500)
        pmd.Update(axis)
        status = pmd.GetActivityStatus(axis)
        while status.in_motion:
            status = pmd.GetActivityStatus(axis)
        expected = 100
        received = pmd.GetPositionError(axis)
        assert (received == expected), f'GetPositionError() expected {expected}, received {received}'
        pmd.ClearPositionError(axis)
        pmd.Update(axis)
        expected = 0
        received = pmd.GetPositionError(axis)
        assert (received == expected), f'GetPositionError() expected {expected}, received {received}'
    print('passed')

    print('testing RestoreOperatingMode...', end='', flush=True)
    for axis in PMDAxis:
        pmd.SetEventAction(axis, PMDEvent.MOTION_ERROR, PMDAction.DISABLE_POSITION_LOOP)
        pmd.SetPositionErrorLimit(axis, 50)
        pmd.SetPosition(axis, 500)
        pmd.Update(axis)
        status = pmd.GetActivityStatus(axis)
        while status.in_motion:
            status = pmd.GetActivityStatus(axis)
        status = pmd.GetEventStatus(axis)
        assert(status & PMDEventStatus.MOTION_ERROR), 'GetEventStatus() expected MOTION_ERROR=True, found False'
        pmd.ResetEventStatus(axis, ~PMDEventStatus.MOTION_ERROR)
        pmd.SetPositionErrorLimit(axis, 65535)
        pmd.ResetEventStatus(axis, PMDEventStatus(0))
        pmd.SetVelocity(axis, velocity)
        pmd.SetPosition(axis, 500)
        pmd.Update(axis)
        status = pmd.GetActivityStatus(axis)
        while status.in_motion:
            status = pmd.GetActivityStatus(axis)
        expected = 0
        received = pmd.GetPositionError(axis)
        assert (received == expected), f'GetPositionError() expected {expected}, received {received}'
        pmd.ResetEventStatus(axis, PMDEventStatus(0))
        pmd.RestoreOperatingMode(axis)
        pmd.SetVelocity(axis, velocity)
        pmd.SetPosition(axis, 500)
        pmd.Update(axis)
        status = pmd.GetActivityStatus(axis)
        while status.in_motion:
            status = pmd.GetActivityStatus(axis)
        expected = 100
        received = pmd.GetPositionError(axis)
        assert (received == expected), f'GetPositionError() expected {expected}, received {received}'
        pmd.ClearPositionError(axis)
        pmd.Update(axis)
        pmd.ResetEventStatus(axis, PMDEventStatus(0))
        pmd.SetEncoderSource(axis, PMDEncoderSource.LOOPBACK)
        pmd.SetEventAction(axis, PMDEvent.MOTION_ERROR, PMDAction.NONE)
    print('passed')

    print('test Read/WriteIO...', end='', flush=True)
    motor1_drive_amps = pmd.ReadIO(2)
    motor2_drive_amps = pmd.ReadIO(6)
    expected1 = 0x0123
    pmd.WriteIO(2, expected1)
    expected2 = 0x4567
    pmd.WriteIO(6, expected2)
    received1 = pmd.ReadIO(2)
    assert(received1 == expected1), f'ReadIO() expected {expected1}, received {received1}'
    received2 = pmd.ReadIO(6)
    assert(received2 == expected2), f'ReadIO() expected {expected2}, received {received2}'
    pmd.WriteIO(2, motor1_drive_amps)
    pmd.WriteIO(6, motor2_drive_amps)
    print('passed')

    print('\nAll tests passed successfully.')
