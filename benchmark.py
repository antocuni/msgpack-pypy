import time
import random
import msgpack
import msgpack_pypy

try:
    import __pypy__
    is_pypy = True
except ImportError:
    is_pypy = False

N = 2000
def bench(module, obj):
    def run():
        t = []
        for i in range(N):
            a = time.time()
            x = module.dumps(obj)
            b = time.time()
            t.append(b-a)
        dump_avg = sum(t)/len(t) * 1000
        #
        t = []
        for i in range(N):
            a = time.time()
            obj2 = module.loads(x)
            b = time.time()
            t.append(b-a)
        load_avg = sum(t)/len(t) * 1000
        return dump_avg, load_avg, len(x)

    if is_pypy:
        run() # warmup
    dump_avg, load_avg, length = run()
    print '%14s: dump: %.4f ms     load: %.4f ms    len: %d bytes' % (
        module.__name__, dump_avg, load_avg, length)


def main():
    print 'list of ints'
    obj = [random.randrange(0, 20000) for i in range(10000)]
    bench(msgpack, obj)
    bench(msgpack_pypy, obj)
    print

    print 'list of floats'
    obj = [random.random() for i in range(10000)]
    bench(msgpack, obj)
    bench(msgpack_pypy, obj)

if __name__ == '__main__':
    main()
