import random
import arrow
from hashlib import md5
import re
now = arrow.now()
time_int = int(now.timestamp())

rand = str(random.random())
md5_string=md5(str(str(time_int)+rand).encode()).hexdigest()

def D(e, t, o):
    e = "/" + "/".join(filter(None, e.split("/"))) + "/"
    i = ""
    n = "JKMNPQRTX1234OABCDFG56789H"

    def O():
        return lambda x: x

    r = md5("".join(filter(lambda x: re.match(r'[0-9]', x), str(o + n))).encode()).hexdigest()
    l = "".join(filter(lambda x: re.match(r'[0-9]', x), md5(str(t + e + r).encode()).hexdigest()))[:9]

    l = l.ljust(9, '0')

    c = int(l)
    for s in range(5):
        p = c % len(n)
        c = c // len(n)
        i += n[p]

    def y(e):
        return 255 & (e << 1 ^ 27) if 128 & e else e << 1

    def F(e):
        return y(e) ^ e

    def E(e):
        return F(y(e))

    def z(e):
        return E(F(y(e)))

    def A(e):
        return z(e) ^ E(e) ^ F(e)

    def custom_function(arr):
        t = [0, 0, 0, 0]
        t[0] = A(arr[0]) ^ z(arr[1]) ^ E(arr[2]) ^ F(arr[3])
        t[1] = F(arr[0]) ^ A(arr[1]) ^ z(arr[2]) ^ E(arr[3])
        t[2] = E(arr[0]) ^ F(arr[1]) ^ A(arr[2]) ^ z(arr[3])
        t[3] = z(arr[0]) ^ E(arr[1]) ^ F(arr[2]) ^ A(arr[3])
        arr[0] = t[0]
        arr[1] = t[1]
        arr[2] = t[2]
        arr[3] = t[3]
        return arr

    d = str(sum(custom_function(list(map(ord, i[-4:])))))[1:]
    if len(str(d)) < 2:
        d = "0" + str(d)
    d = i + str(d)
    dic = {
        'hkey':d,
        'nonce':o,
        "_time":int(t)-1
    }
    return dic
