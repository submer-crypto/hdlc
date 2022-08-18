from hdlc import Receiver, SFrame, IFrame, FRAME_SUPERVISORY, SUPERVISORY_RECEIVE_READY
import pytest

def test_write_overflow():
    receiver = Receiver(buffer_length=64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    with pytest.raises(ValueError, match='Buffer length exceeded'):
        receiver.write(bytearray(65))

def test_write_read():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'~\xaaptest\xe6\xb0~')

    assert receiver.length == 10
    assert receiver.available_length == 54

    read = receiver.read(buffer)

    assert read == 4
    assert buffer[0:4] == b'test'

    read = receiver.read(buffer)

    assert read == 0
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_write_read_supervisory_frame():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'~\xaa!Cm~')

    assert receiver.length == 6
    assert receiver.available_length == 58

    read = receiver.read(buffer)

    assert read == 0
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_write_read_raw_supervisory_frame():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'~\xaa!Cm~')

    assert receiver.length == 6
    assert receiver.available_length == 58

    read, frame, valid = receiver.read_frame(buffer)

    assert read == 0
    assert valid
    assert frame is not None
    assert isinstance(frame, SFrame)
    assert frame.address == 0xAA
    assert not frame.poll_final
    assert frame.frame_type == FRAME_SUPERVISORY
    assert frame.receive_sequence_number == 1
    assert frame.supervisory_type == SUPERVISORY_RECEIVE_READY

    read, frame, valid = receiver.read_frame(buffer)

    assert read == 0
    assert frame is None
    assert not valid
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_chunked_write_read():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'~\xaaptest')

    assert receiver.length == 7
    assert receiver.available_length == 57

    read = receiver.read(buffer)

    assert read == 0

    receiver.write(b'\xe6\xb0~')

    assert receiver.length == 10
    assert receiver.available_length == 54

    read = receiver.read(buffer)

    assert read == 4
    assert buffer[0:4] == b'test'

    read = receiver.read(buffer)

    assert read == 0
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_garbage_start_write_read():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'garbage~\xaaptest\xe6\xb0~')

    assert receiver.length == 17
    assert receiver.available_length == 47

    read = receiver.read(buffer)

    assert read == 4
    assert buffer[0:4] == b'test'

    read = receiver.read(buffer)

    assert read == 0
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_garbage_middle_write_read():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'~\xaaptest 1\xbc\x04~garbage~\xaartest 2\x9c\x01~')

    assert receiver.length == 31
    assert receiver.available_length == 33

    read = receiver.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'test 1'
    assert receiver.length == 20
    assert receiver.available_length == 44

    read = receiver.read(buffer)

    # By default receiver returns data
    # of invalid frames
    assert read == 5
    assert buffer[0:5] == b'rbage'
    assert receiver.length == 12
    assert receiver.available_length == 52

    read = receiver.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'test 2'
    assert receiver.length == 1
    assert receiver.available_length == 63

    read = receiver.read(buffer)

    assert read == 0
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_garbage_middle_write_read_raw():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'~\xaaptest 1\xbc\x04~garbage~\xaartest 2\x9c\x01~')

    assert receiver.length == 31
    assert receiver.available_length == 33

    read, frame, valid = receiver.read_frame(buffer)

    assert read == 6
    assert valid
    assert frame is not None
    assert isinstance(frame, IFrame)
    assert buffer[0:6] == b'test 1'
    assert receiver.length == 20
    assert receiver.available_length == 44

    read, frame, valid = receiver.read_frame(buffer)

    assert read == 5
    assert not valid
    assert frame is not None
    assert buffer[0:5] == b'rbage'
    assert receiver.length == 12
    assert receiver.available_length == 52

    read, frame, valid = receiver.read_frame(buffer)

    assert read == 6
    assert valid
    assert frame is not None
    assert isinstance(frame, IFrame)
    assert buffer[0:6] == b'test 2'
    assert receiver.length == 1
    assert receiver.available_length == 63

    read, frame, valid = receiver.read_frame(buffer)

    assert read == 0
    assert frame is None
    assert not valid
    assert receiver.length == 1
    assert receiver.available_length == 63

def test_garbage_only_write_read():
    receiver = Receiver(buffer_length=64)
    buffer = bytearray(64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    receiver.write(b'garbage')

    assert receiver.length == 7
    assert receiver.available_length == 57

    read = receiver.read(buffer)

    assert read == 0
    assert receiver.length == 0
    assert receiver.available_length == 64
