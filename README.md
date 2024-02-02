# HDLC

A Python library for encoding and decoding [HDLC](https://en.wikipedia.org/wiki/High-Level_Data_Link_Control) frames and facilitating transport agnostic communication. Based on the C++ implementation [bang-olufsen/hdlcpp](https://github.com/bang-olufsen/hdlcpp) but is not necessarily compatible with the C++ library.

## Usage

Initiate a receiver and sender pair using the `protocol` function for respectively decoding and encoding HDLC frames. The pair is linked, the sender might have queued up messages pending depending on what is written to the receiver.

```python
from hdlc import protocol, TimeoutError, NORMAL_RESPONSE_MODE

buffer = bytearray(2048)
receiver, sender = protocol(True, 0xAA,
    buffer_length=1024,
    write_timeout_ms=1000,
    write_retries=2,
    mode=NORMAL_RESPONSE_MODE)

# Write bytes received from the remote node
# to the receiver.
receiver.write(b'...')

while (read := receiver.read(buffer)) > 0:
    # Buffer contains data sent by the remote node
    print(buffer[0:read])

sender.write(b'hello')

# Read data to send to the remote node.
# The second parameter specifies how much time has elapsed
# since the last time the read method was called.
# Used to calculate if a frame has timed out and needs to be resent.
try:
    while (read := sender.read(buffer, delta_ms=delta_ms)) > 0:
        io_send(buffer[0:read])
except TimeoutError as e:
    print('No ack received within timeout', e)
```

The API is designed for single threaded, non-blocking usage. Care must be taken not to access the receiver or sender from different threads at the same time.
