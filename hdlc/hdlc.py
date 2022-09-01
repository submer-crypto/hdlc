import heapq

FRAME_INFORMATION = 0
FRAME_SUPERVISORY = 1
FRAME_UNNUMBERED = 2

SUPERVISORY_RECEIVE_READY = 0x00
SUPERVISORY_RECEIVE_NOT_READY = 0x02
SUPERVISORY_REJECT = 0x01
SUPERVISORY_SELECTIVE_REJECT = 0x03

UNNUMBERED_DISCONNECTED_MODE = 0x03
UNNUMBERED_ACKNOWLEDGE = 0x0C
UNNUMBERED_SET_NORMAL_RESPONSE_MODE = 0x08
UNNUMBERED_SET_ASYNCHRONOUS_RESPONSE_MODE = 0x07
UNNUMBERED_SET_ASYNCHRONOUS_BALANCED_MODE = 0x07
UNNUMBERED_DISCONNECT = 0x04
UNNUMBERED_REQUEST_DISCONNECT = 0x04
UNNUMBERED_SET_INITIALIZATION_MODE = 0x09
UNNUMBERED_REQUEST_INITIALIZATION_MODE = 0x01
UNNUMBERED_FRAME_REJECT_RESPONSE = 0x11
UNNUMBERED_RESET = 0x0B

NORMAL_RESPONSE_MODE = 0x00
ASYNCHRONOUS_RESPONSE_MODE = 0x01
ASYNCHRONOUS_BALANCED_MODE = 0x02

_BUFFER_0 = bytearray(0)

_FLAG_BYTE = 0x7E
_ESCAPE_BYTE = 0x7D
_FCS_INITIAL = 0xFFFF
_FCS_TARGET = 0xF0B8

_CRC16_TABLE = (
    0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
    0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
    0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
    0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
    0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
    0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
    0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
    0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
    0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
    0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
    0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
    0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
    0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
    0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
    0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
    0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
    0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
    0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
    0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
    0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
    0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
    0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
    0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
    0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
    0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
    0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
    0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
    0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
    0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
    0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
    0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
    0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
)

def crc16(acc, value):
    return (acc >> 8) ^ (_CRC16_TABLE[(acc ^ value) & 0xFF])

def copy(source, destination, source_offset, destination_offset, length):
    for i in range(length):
        destination[destination_offset + i] = source[source_offset + i]

def heappop(heap, i):
    item = heap[i]
    heap[i] = heap[-1]
    heap.pop()
    heapq.heapify(heap)
    return item

class Frame:
    def __init__(self, address, poll_final, frame_type):
        self.address = address
        self.poll_final = poll_final
        self.frame_type = frame_type

class IFrame(Frame):
    def __init__(self, address, receive_sequence_number, poll_final, send_sequence_number):
        super().__init__(address, poll_final, FRAME_INFORMATION)

        self.receive_sequence_number = receive_sequence_number
        self.send_sequence_number = send_sequence_number

    def __repr__(self):
        return (f'IFrame({hex(self.address)}, {self.receive_sequence_number}, '
                + f'{self.poll_final}, {self.send_sequence_number})')

class SFrame(Frame):
    def __init__(self, address, receive_sequence_number, poll_final, supervisory_type):
        super().__init__(address, poll_final, FRAME_SUPERVISORY)

        self.receive_sequence_number = receive_sequence_number
        self.supervisory_type = supervisory_type

    def __repr__(self):
        return (f'SFrame({hex(self.address)}, {self.receive_sequence_number}, '
                + f'{self.poll_final}, {hex(self.supervisory_type)})')

class UFrame(Frame):
    def __init__(self, address, unnumbered_type, poll_final):
        super().__init__(address, poll_final, FRAME_UNNUMBERED)

        self.unnumbered_type = unnumbered_type

    def __repr__(self):
        return f'UFrame({hex(self.address)}, {self.unnumbered_type}, {self.poll_final})'

def escape(value, buffer, offset):
    if value == _FLAG_BYTE or value == _ESCAPE_BYTE:
        buffer[offset] = _ESCAPE_BYTE
        buffer[offset + 1] = value ^ 0x20
        return 2

    buffer[offset] = value
    return 1

def encode_frame(frame, buffer, offset, length, frame_buffer):
    frame_index = 1
    fcs = _FCS_INITIAL

    frame_buffer[0] = _FLAG_BYTE

    value = frame.address
    fcs = crc16(fcs, value)
    frame_index += escape(value, frame_buffer, frame_index)

    value = encode_control(frame)
    fcs = crc16(fcs, value)
    frame_index += escape(value, frame_buffer, frame_index)

    for i in range(length):
        value = buffer[offset + i]
        fcs = crc16(fcs, value)
        frame_index += escape(value, frame_buffer, frame_index)

    fcs ^= 0xFFFF

    value = fcs & 0xFF
    frame_index += escape(value, frame_buffer, frame_index)

    value = (fcs >> 8) & 0xFF
    frame_index += escape(value, frame_buffer, frame_index)

    frame_buffer[frame_index] = _FLAG_BYTE

    return frame_index + 1

def encode_control(frame):
    value = 0

    if frame.frame_type == FRAME_INFORMATION:
        value |= (frame.receive_sequence_number & 0x07) << 5
        value |= (1 if frame.poll_final else 0) << 4
        value |= (frame.send_sequence_number & 0x07) << 1
    elif frame.frame_type == FRAME_SUPERVISORY:
        value |= (frame.receive_sequence_number & 0x07) << 5
        value |= (1 if frame.poll_final else 0) << 4
        value |= (frame.supervisory_type & 0x03) << 2
        value |= 0x01
    else:
        value |= (frame.unnumbered_type & 0x1C) << 3
        value |= (1 if frame.poll_final else 0) << 4
        value |= (frame.unnumbered_type & 0x03) << 2
        value |= 0x03

    return value

def decode_frame(buffer, length, information_buffer):
    information_index = 0
    frame_start_index = -1
    frame_end_index = -1
    control_escape = False
    fcs = _FCS_INITIAL
    frame = None

    for i in range(length):
        if frame_start_index < 0:
            if buffer[i] == _FLAG_BYTE:
                if i < length - 1 and buffer[i + 1] == _FLAG_BYTE:
                    continue

                frame_start_index = i
        else:
            if buffer[i] == _FLAG_BYTE:
                frame_end_index = i
                break
            elif buffer[i] == _ESCAPE_BYTE:
                control_escape = True
            else:
                value = buffer[i]

                if control_escape:
                    control_escape = False
                    value = value ^ 0x20

                fcs = crc16(fcs, value)

                if i == frame_start_index + 2:
                    address = buffer[frame_start_index + 1]
                    frame = decode_control(address, value)
                elif i > frame_start_index + 2:
                    information_buffer[information_index] = value
                    information_index += 1

    if frame_start_index < 0:
        return (length, 0, None, False)
    elif frame_end_index < 0:
        return (0, 0, None, False)
    elif frame_start_index + 4 > frame_end_index or control_escape or fcs != _FCS_TARGET:
        return (frame_end_index, information_index, frame, False)
    else:
        return (frame_end_index, information_index - 2, frame, True)

def decode_control(address, value):
    if value & 0x01 == 0:
        receive_sequence_number = (value >> 5) & 0x07
        poll_final = True if (value >> 4) & 0x01 == 1 else False
        send_sequence_number = (value >> 1) & 0x07
        return IFrame(address, receive_sequence_number, poll_final, send_sequence_number)
    elif value & 0x02 == 0:
        receive_sequence_number = (value >> 5) & 0x07
        poll_final = True if (value >> 4) & 0x01 == 1 else False
        supervisory_type = (value >> 2) & 0x03
        return SFrame(address, receive_sequence_number, poll_final, supervisory_type)
    else:
        unnumbered_type = ((value >> 3) & 0x1C) | ((value >> 2) & 0x03)
        poll_final = True if (value >> 4) & 0x01 == 1 else False
        return UFrame(address, unnumbered_type, poll_final)

def to_unnumbered_type(mode):
    if mode == NORMAL_RESPONSE_MODE:
        return UNNUMBERED_SET_NORMAL_RESPONSE_MODE
    elif mode == ASYNCHRONOUS_RESPONSE_MODE:
        return UNNUMBERED_SET_ASYNCHRONOUS_RESPONSE_MODE
    elif mode == ASYNCHRONOUS_BALANCED_MODE:
        return UNNUMBERED_SET_ASYNCHRONOUS_BALANCED_MODE

    raise ValueError('Unknown operation mode')

class HdlcError(Exception):
    pass

class TimeoutError(HdlcError):
    pass

class Receiver:
    def __init__(self, buffer_length=128):
        self.buffer = bytearray(buffer_length)
        self.length = 0

    @property
    def available_length(self):
        return len(self.buffer) - self.length

    def reset(self):
        self.length = 0

    def write(self, buffer, offset=0, length=None):
        if length is None:
            length = len(buffer) - offset

        if length > self.available_length:
            raise ValueError('Buffer length exceeded')

        copy(buffer, self.buffer, offset, self.length, length)
        self.length += length

    def read_frame(self, information_buffer):
        while True:
            discard_length, information_length, frame, valid = decode_frame(
                self.buffer, self.length, information_buffer)

            if discard_length > 0:
                self.length = self.length - discard_length
                copy(self.buffer, self.buffer, discard_length, 0, self.length)

            if frame is not None:
                return (information_length, frame, valid)

            if discard_length == 0:
                return (0, None, False)

    def read(self, information_buffer):
        raise NotImplementedError()

class ProtocolReceiver(Receiver):
    def __init__(self, sender, master, address, mode, buffer_length=128):
        super().__init__(buffer_length)
        self.sender = sender
        self.master = master
        self.address = address
        self.mode = mode
        self.sequence_number = 0
        self.initialized = False

        if master:
            sender.write_frame(UFrame(address, to_unnumbered_type(mode), True), priority=3, retry=True)

    def reset(self):
        super().reset()
        self.sequence_number = 0
        self.initialized = False

    def read(self, information_buffer):
        while True:
            information_length, frame, valid = self.read_frame(information_buffer)

            if frame is None:
                return 0

            if frame.address == self.address:
                if not self.initialized and self.master:
                    if (frame.frame_type == FRAME_UNNUMBERED
                            and frame.unnumbered_type == UNNUMBERED_ACKNOWLEDGE and valid):
                        self.sender.remove_unnumbered_frame(to_unnumbered_type(self.mode))
                        self.initialized = True
                elif (frame.frame_type == FRAME_UNNUMBERED
                        and (frame.unnumbered_type == UNNUMBERED_SET_NORMAL_RESPONSE_MODE
                            or frame.unnumbered_type == UNNUMBERED_SET_ASYNCHRONOUS_RESPONSE_MODE
                            or frame.unnumbered_type == UNNUMBERED_SET_ASYNCHRONOUS_BALANCED_MODE)
                        and valid):
                    self.reset()
                    self.sender.reset()
                    self.sender.write_frame(UFrame(frame.address, UNNUMBERED_ACKNOWLEDGE, True), priority=1)
                    self.initialized = True
                elif not self.initialized:
                    if valid:
                        self.sender.write_frame(UFrame(frame.address, UNNUMBERED_DISCONNECTED_MODE, True), priority=1)
                elif (frame.frame_type == FRAME_SUPERVISORY
                        and frame.supervisory_type == SUPERVISORY_RECEIVE_READY and valid):
                    self.sender.remove_information_frame(frame.receive_sequence_number)
                elif (frame.frame_type == FRAME_SUPERVISORY
                        and frame.supervisory_type == SUPERVISORY_SELECTIVE_REJECT and valid):
                    # The frame will be resent after timeout is reached
                    pass
                elif frame.frame_type == FRAME_INFORMATION:
                    if valid and frame.send_sequence_number == self.sequence_number:
                        self.sequence_number = (self.sequence_number + 1) % 8
                        response_frame = SFrame(frame.address, self.sequence_number, False, SUPERVISORY_RECEIVE_READY)
                    else:
                        response_frame = SFrame(frame.address, self.sequence_number, True, SUPERVISORY_SELECTIVE_REJECT)
                        information_length = 0

                    self.sender.write_frame(response_frame, priority=1)
                    return information_length

class Sender:
    class _WriteItem:
        def __init__(self, offset, length, frame, priority, retry):
            self.offset = offset
            self.length = length
            self.frame = frame
            self.priority = priority
            self.retry = retry
            self.age_ms = 0
            self.write_count = 0

        def __lt__(self, other):
            return -self.priority < -other.priority

    def __init__(self, buffer_length=128, write_retries=1, write_timeout_ms=500):
        self.write_retries = write_retries
        self.write_timeout_ms = write_timeout_ms
        self.buffer = bytearray(buffer_length)
        self.length = 0
        self.frames = []
        self.sequence_number = 0

    @property
    def available_length(self):
        return len(self.buffer) - self.length

    def reset(self):
        self.length = 0
        self.frames = []
        self.sequence_number = 0

    def write_frame(self, frame, buffer=_BUFFER_0, offset=0, length=None, priority=0, retry=False):
        if length is None:
            length = len(buffer) - offset

        if length > self.available_length:
            raise ValueError('Buffer length exceeded')

        copy(buffer, self.buffer, offset, self.length, length)
        heapq.heappush(self.frames, Sender._WriteItem(self.length, length, frame, priority, retry))
        self.length += length

    def write(self, buffer, offset=0, length=None, address=0xFF, receive_sequence_number=0, poll_final=True):
        frame = IFrame(address, receive_sequence_number, poll_final, self.sequence_number)
        self.sequence_number = (self.sequence_number + 1) % 8
        return self.write_frame(frame, buffer, offset, length, 0, True)

    def read(self, frame_buffer, delta_ms=0):
        if len(self.frames) > 0:
            item = self.frames[0]

            if item.write_count == 0:
                item.write_count += 1
            else:
                item.age_ms += delta_ms

                if item.age_ms < self.write_timeout_ms:
                    return 0
                else:
                    item.age_ms = 0
                    item.write_count += 1

            if item.write_count > self.write_retries + 1:
                self._remove_frame(0)
                raise TimeoutError('Did not receive ack within timeout')

            frame_length = encode_frame(item.frame, self.buffer, item.offset, item.length, frame_buffer)

            if not item.retry:
                self._remove_frame(0)

            return frame_length

        return 0

    def remove_information_frame(self, receive_sequence_number):
        for i, item in enumerate(self.frames):
            if (item.frame.frame_type == FRAME_INFORMATION
                    and item.write_count > 0
                    and item.frame.send_sequence_number == receive_sequence_number - 1):
                self._remove_frame(i)
                return

    def remove_unnumbered_frame(self, unnumbered_type):
        for i, item in enumerate(self.frames):
            if (item.frame.frame_type == FRAME_UNNUMBERED
                    and item.write_count > 0
                    and item.frame.unnumbered_type == unnumbered_type):
                self._remove_frame(i)
                return

    def _remove_frame(self, i):
        item = heappop(self.frames, i)
        self.length = self.length - item.length
        copy(self.buffer, self.buffer, item.offset + item.length, item.offset, self.length - item.offset)

class ProtocolSender(Sender):
    def __init__(self, address, buffer_length=128, write_retries=1, write_timeout_ms=500):
        super().__init__(buffer_length, write_retries, write_timeout_ms)
        self.address = address

    def write(self, buffer, offset=0, length=None, address=None, receive_sequence_number=0, poll_final=True):
        if address is None:
            address = self.address

        return super().write(buffer, offset, length, address, receive_sequence_number, poll_final)

def protocol(master, address, buffer_length=128, write_timeout_ms=500, write_retries=1, mode=NORMAL_RESPONSE_MODE):
    """Create a receiver and sender pair for respectively decoding and encoding HDLC frames.
    The pair is linked, the sender might have queued up messages pending depending on what is written
    to the receiver.

    :param master: If the instance should act as a master node and initiate the communication
        with the remote node.
    :type master: bool
    :param address: If master is True then this specifies the address of the remote slave node
        (since master nodes don't have explicit addresses). If master is False then this is the address
        of current slave node.
    :type address: int
    :param buffer_length: Length of internal receiver and sender buffers. Writing beyond the specified length
        will result in an error.
    :type buffer_length: int
    :param write_timeout_ms: The write timeout for messages that require acknowledgement, e.g. information frames.
    :type write_timeout_ms: int
    :param write_retries: Number of times to retry a message after the initial write has failed. The message will
        be queued up in the sender again after write_timeout_ms has been reached. If the retry limit is also reached
        class:`hdlc.TimeoutError` is raised instead.
    :type write_retries: int
    """
    sender = ProtocolSender(address, buffer_length, write_retries, write_timeout_ms)
    receiver = ProtocolReceiver(sender, master, address, mode, buffer_length)
    return receiver, sender
