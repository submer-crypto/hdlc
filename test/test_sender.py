from hdlc import TimeoutError, Sender, SFrame, SUPERVISORY_RECEIVE_READY
import pytest

def test_write_overflow():
    sender = Sender(buffer_length=64)

    assert sender.length == 0
    assert sender.available_length == 64

    with pytest.raises(ValueError, match='Buffer length exceeded'):
        sender.write(bytearray(65))

def test_write_read():
    sender = Sender(buffer_length=64)
    buffer = bytearray(64)

    assert sender.length == 0
    assert sender.available_length == 64

    sender.write(b'test', address=0xAA, receive_sequence_number=3, poll_final=True)

    assert sender.length == 4
    assert sender.available_length == 60
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 0
    assert sender.length == 4
    assert sender.available_length == 60

def test_write_read_after_timeout():
    sender = Sender(buffer_length=64, write_retries=1, write_timeout_ms=100)
    buffer = bytearray(64)

    assert sender.length == 0
    assert sender.available_length == 64

    sender.write(b'test', address=0xAA, receive_sequence_number=3, poll_final=True)

    assert sender.length == 4
    assert sender.available_length == 60
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    read = sender.read(buffer, delta_ms=150)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    with pytest.raises(TimeoutError, match='Did not receive ack within timeout'):
        sender.read(buffer, delta_ms=150)

    assert len(sender.frames) == 0
    assert sender.length == 0
    assert sender.available_length == 64

def test_write_read_multiple_after_timeout():
    sender = Sender(buffer_length=64, write_retries=1, write_timeout_ms=100)
    buffer = bytearray(64)

    assert sender.length == 0
    assert sender.available_length == 64

    sender.write(b'test', address=0xAA, receive_sequence_number=3, poll_final=True)

    assert sender.length == 4
    assert sender.available_length == 60
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    read = sender.read(buffer, delta_ms=50)

    assert read == 0

    read = sender.read(buffer, delta_ms=50)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

    with pytest.raises(TimeoutError, match='Did not receive ack within timeout'):
        sender.read(buffer, delta_ms=100)

    assert len(sender.frames) == 0
    assert sender.length == 0
    assert sender.available_length == 64

def test_multiple_write_read():
    sender = Sender(buffer_length=64, write_retries=1, write_timeout_ms=100)
    buffer = bytearray(64)

    assert sender.length == 0
    assert sender.available_length == 64

    sender.write(b'test 1', address=0xAA, receive_sequence_number=3, poll_final=True)
    sender.write(b'test 2', address=0xAA, receive_sequence_number=3, poll_final=True)

    assert sender.length == 12
    assert sender.available_length == 52
    assert len(sender.frames) == 2

    read = sender.read(buffer)

    assert read == 12
    assert buffer[0:12] == b'~\xaaptest 1\xbc\x04~'
    assert len(sender.frames) == 2

    read = sender.read(buffer, delta_ms=150)

    assert read == 12
    assert buffer[0:12] == b'~\xaaptest 1\xbc\x04~'
    assert len(sender.frames) == 2

    with pytest.raises(TimeoutError, match='Did not receive ack within timeout'):
        sender.read(buffer, delta_ms=150)

    assert sender.length == 6
    assert sender.available_length == 58

    read = sender.read(buffer)

    assert read == 12
    assert buffer[0:12] == b'~\xaartest 2\x9c\x01~'
    assert len(sender.frames) == 1
    assert sender.length == 6
    assert sender.available_length == 58

    read = sender.read(buffer, delta_ms=150)

    assert read == 12
    assert buffer[0:12] == b'~\xaartest 2\x9c\x01~'
    assert len(sender.frames) == 1

    with pytest.raises(TimeoutError, match='Did not receive ack within timeout'):
        sender.read(buffer, delta_ms=150)

    assert sender.length == 0
    assert sender.available_length == 64

def test_write_read_ready():
    sender = Sender(buffer_length=64)
    buffer = bytearray(64)

    assert sender.length == 0
    assert sender.available_length == 64

    sender.write_frame(SFrame(0xAA, 1, False, SUPERVISORY_RECEIVE_READY))

    assert sender.length == 0
    assert sender.available_length == 64
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaa!Cm~'
    assert len(sender.frames) == 0

def test_write_read_ready_after_information():
    sender = Sender(buffer_length=64)
    buffer = bytearray(64)

    assert sender.length == 0
    assert sender.available_length == 64

    sender.write(b'test', address=0xAA, receive_sequence_number=3, poll_final=True)
    sender.write_frame(SFrame(0xAA, 1, False, SUPERVISORY_RECEIVE_READY))

    assert sender.length == 4
    assert sender.available_length == 60
    assert len(sender.frames) == 2

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaa!Cm~'
    assert sender.length == 4
    assert sender.available_length == 60
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1
