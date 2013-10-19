import msgpack

try:
    import __pypy__
except ImportError:
    is_pypy = False
else:
    is_pypy = True

INT_LIST = 0
FLOAT_LIST = 1

if is_pypy:
    import cffi
    ffi = cffi.FFI()

    class Packer(msgpack.Packer):
        def _pack(self, obj, *args):
            if isinstance(obj, list):
                strategy = __pypy__.list_strategy(obj)
                if strategy == 'int':
                    # super-fast conversion from list-of-ints to a raw
                    # buffer, only in the pypy fast_cffi_list_init branch for
                    # now
                    buf = ffi.buffer(ffi.new("long[]", obj))
                    # this extra copy should not be needed :-(
                    return self.pack_extended_type(INT_LIST, buf[:])
                elif strategy == 'float':
                    # same as above
                    buf = ffi.buffer(ffi.new("double[]", obj))
                    return self.pack_extended_type(FLOAT_LIST, buf[:])
            return msgpack.Packer._pack(self, obj, *args)

    class Unpacker(msgpack.Unpacker):
        def read_extended_type(self, typecode, data):
            if typecode == INT_LIST:
                N = len(data)/8 # XXX: 4 on 32bit
                chars = ffi.new("char[]", data)
                ints = ffi.cast("long[%d]" % N, chars)
                return list(ints)
            elif typecode == FLOAT_LIST:
                N = len(data)/8
                chars = ffi.new("char[]", data)
                floats = ffi.cast("double[%d]" % N, chars)
                return list(floats)
            else:
                msgpack.Unpacker.read_extended_type(self, typecode, data)

else: # CPython version
    import array
    
    Packer = msgpack.Packer

    class Unpacker(msgpack.Unpacker):
        def read_extended_type(self, typecode, data):
            if typecode == INT_LIST:
                ints = array.array('l')
                ints.fromstring(data)
                return list(ints)
            if typecode == FLOAT_LIST:
                floats = array.array('d')
                floats.fromstring(data)
                return list(floats)
            else:
                msgpack.Unpacker.read_extended_type(self, typecode, data)


def pack(o, stream, **kwargs):
    """
    Pack object `o` and write it to `stream`

    See :class:`Packer` for options.
    """
    packer = Packer(**kwargs)
    stream.write(packer.pack(o))

def packb(o, **kwargs):
    """
    Pack object `o` and return packed bytes

    See :class:`Packer` for options.
    """
    return Packer(**kwargs).pack(o)

def unpack(stream, **kwargs):
    """
    Unpack an object from `stream`.

    Raises `ExtraData` when `packed` contains extra bytes.
    See :class:`Unpacker` for options.
    """
    unpacker = Unpacker(stream, **kwargs)
    return unpacker.unpack_one()

def unpackb(packed, **kwargs):
    """
    Unpack an object from `packed`.

    Raises `ExtraData` when `packed` contains extra bytes.
    See :class:`Unpacker` for options.
    """
    unpacker = Unpacker(None, **kwargs)
    unpacker.feed(packed)
    return unpacker.unpack_one()
