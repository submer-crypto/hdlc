from hdlc import Receiver
import pytest

def test_write_overflow():
    receiver = Receiver(buffer_length=64)

    assert receiver.length == 0
    assert receiver.available_length == 64

    with pytest.raises(ValueError, match='Buffer length exceeded'):
        receiver.write(bytearray(65))
