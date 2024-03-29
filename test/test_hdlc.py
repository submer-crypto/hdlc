from hdlc import TimeoutError, protocol, NORMAL_RESPONSE_MODE
import pytest

def test_handshake_block_send():
    receiver, sender = protocol(True, 0xAA, write_timeout_ms=100, write_retries=1, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    sender.write(b'test', receive_sequence_number=3, poll_final=True)

    assert len(sender.frames) == 2

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 2

    read = sender.read(buffer)

    assert read == 0

    read = sender.read(buffer, delta_ms=150)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 2

    receiver.write(b'~\xaas\xd4\x1c~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1
    assert receiver.initialized

    read = sender.read(buffer)

    assert read == 10
    assert buffer[0:10] == b'~\xaaptest\xe6\xb0~'
    assert len(sender.frames) == 1

def test_handshake_timeout():
    receiver, sender = protocol(True, 0xAA, write_timeout_ms=100, write_retries=1, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    sender.write(b'test', receive_sequence_number=3, poll_final=True)

    assert len(sender.frames) == 2

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 2

    read = sender.read(buffer)

    assert read == 0

    read = sender.read(buffer, delta_ms=150)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 2

    with pytest.raises(TimeoutError, match='Did not receive ack within timeout'):
        sender.read(buffer, delta_ms=150)

    assert len(sender.frames) == 1

def test_receive_valid_frame():
    receiver, sender = protocol(True, 0xAA, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaas\xd4\x1c~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0
    assert receiver.initialized

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
    receiver, sender = protocol(True, 0xAA, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaas\xd4\x1c~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0
    assert receiver.initialized

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

def test_receive_valid_frame_with_bad_address():
    receiver, sender = protocol(True, 0xBB, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xbbS\x9f\xb1~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xbbs\x9d\x90~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0
    assert receiver.initialized

    receiver.write(b'~\xaaptest\xe6\xb0~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0

def test_receive_ready():
    receiver, sender = protocol(True, 0xAA, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaas\xd4\x1c~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0
    assert receiver.initialized

    sender.write(b'test', receive_sequence_number=3, poll_final=True)
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
    receiver, sender = protocol(True, 0xAA, write_timeout_ms=100, write_retries=1, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaas\xd4\x1c~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0
    assert receiver.initialized

    sender.write(b'test', receive_sequence_number=3, poll_final=True)
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
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 0

def test_receive_valid_frame_with_overflowing_sequence_number():
    receiver, sender = protocol(True, 0xAA, mode=NORMAL_RESPONSE_MODE)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaaS\xd6=~'
    assert len(sender.frames) == 1

    receiver.write(b'~\xaas\xd4\x1c~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0
    assert receiver.initialized

    for i in range(8):
        message = b'test ' + bytes(str(i + 1), encoding='utf8')

        sender.write(message)
        read = sender.read(buffer)

        assert read == 12
        assert len(sender.frames) == 1

        # Cheat by writting own message to receiver
        # so we can get the acknowledge frame
        receiver.write(buffer, 0, read)
        read = receiver.read(buffer)

        assert read == 6
        assert buffer[0:6] == message
        assert len(sender.frames) == 2

        # Read acknowledge frame
        read = sender.read(buffer)

        assert read == 6
        assert len(sender.frames) == 1

        # Write acknowledge frame which removes
        # the pending information frame from the queue
        receiver.write(buffer, 0, read)
        read = receiver.read(buffer)

        assert read == 0
        assert len(sender.frames) == 0

def test_slave_disconnect_mode():
    receiver, sender = protocol(False, 0xAA)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 0

    receiver.write(b'~\xaaptest\xe6\xb0~')
    read = receiver.read(buffer)

    assert read == 0
    assert not receiver.initialized
    assert len(sender.frames) == 1

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaa\x1f\xbe\xb5~'
    assert len(sender.frames) == 0

def test_slave_reset():
    receiver, sender = protocol(False, 0xAA)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 0

    receiver.write(b'~\xaaS\xd6=~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1
    assert receiver.initialized
    assert receiver.sequence_number == 0
    assert sender.sequence_number == 0

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaas\xd4\x1c~'

    receiver.write(b'~\xaaptest 1\xbc\x04~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'test 1'
    assert len(sender.frames) == 1

    sender.write(b'test 2')

    assert len(sender.frames) == 2
    assert receiver.sequence_number == 1
    assert sender.sequence_number == 1

    receiver.write(b'~\xaaS\xd6=~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1
    assert receiver.initialized
    assert receiver.sequence_number == 0
    assert sender.sequence_number == 0

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaas\xd4\x1c~'

def test_slave_receive_valid_frame():
    receiver, sender = protocol(False, 0xAA)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 0

    receiver.write(b'~\xaaS\xd6=~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1
    assert receiver.initialized

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xaas\xd4\x1c~'

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
    receiver, sender = protocol(False, 0xBB)
    buffer = bytearray(128)

    assert not receiver.initialized
    assert len(sender.frames) == 0

    receiver.write(b'~\xbbS\x9f\xb1~')
    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 1
    assert receiver.initialized

    read = sender.read(buffer)

    assert read == 6
    assert buffer[0:6] == b'~\xbbs\x9d\x90~'

    receiver.write(b'~\xaaptest\xe6\xb0~')

    assert len(sender.frames) == 0

    read = receiver.read(buffer)

    assert read == 0
    assert len(sender.frames) == 0

    read = sender.read(buffer)

    assert read == 0
