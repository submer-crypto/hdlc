from hdlc import protocol
import pytest

def test_receive_valid_frame():
    receiver, sender = protocol(True)
    buffer = bytearray(128)

    receiver.write(b'~\xaaptest\xe6\xb0~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 4
    assert buffer[0:4] == b'test'
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaa!Cm~'
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0

def test_receive_invalid_frame():
    receiver, sender = protocol(True)
    buffer = bytearray(128)

    receiver.write(b'~\xaaptest\xe6\x00~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaa\x1d\xac\x96~'
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0

def test_receive_ready():
    receiver, sender = protocol(True)
    buffer = bytearray(128)

    assert len(sender.frames) == 0

    sender.write(b'test', address=0xAA, receive_sequence_number=3, poll_final=True)
    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaa!Cm~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0

def test_receive_reject():
    receiver, sender = protocol(True, write_timeout_ms=100, write_retries=1)
    buffer = bytearray(128)

    assert len(sender.frames) == 0

    sender.write(b'test', address=0xAA, receive_sequence_number=3, poll_final=True)
    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaa\x1d\xac\x96~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1

    read = sender.read(buffer, delta_ms=150)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0

def test_slave_receive_valid_frame():
    receiver, sender = protocol(False, address=0xAA)
    buffer = bytearray(128)

    receiver.write(b'~\xaaptest\xe6\xb0~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 4
    assert buffer[0:4] == b'test'
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaa!Cm~'
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0

def test_slave_receive_valid_frame_with_bad_address():
    receiver, sender = protocol(False, address=0xBB)
    buffer = bytearray(128)

    receiver.write(b'~\xaaptest\xe6\xb0~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0
