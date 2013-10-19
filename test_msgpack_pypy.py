import msgpack_pypy
from msgpack_pypy import is_pypy

def test_pack_unpack_ints():
    obj = [1, 2, 3]
    s = msgpack_pypy.packb(obj)
    assert msgpack_pypy.unpackb(s) == obj
    if is_pypy:
        assert s[0] == '\xc7' # extended type

def test_unpack_ints():
    # make sure that CPython can properly decode the ext type
    s = '\xc7\x18\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00'
    assert msgpack_pypy.unpackb(s) == [1, 2, 3]

def test_pack_unpack_floats():
    obj = [1.1, 2.2, 3.3]
    s = msgpack_pypy.packb(obj)
    assert msgpack_pypy.unpackb(s) == obj
    if is_pypy:
        assert s[0] == '\xc7' # extended type

def test_unpack_floats():
    # make sure that CPython can properly decode the ext type
    s = '\xc7\x18\x01\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@ffffff\n@'
    assert msgpack_pypy.unpackb(s) == [1.1, 2.2, 3.3]

