from rx import operators as op

from giving.gvn import Stream

s = Stream()
s.source.pipe(op.max_by(key_mapper=lambda x: -x)).print()

s.push(1)
s.push(2)
s.push(-4)
s.complete()

s.source.pipe(op.max_by(key_mapper=lambda x: -x)).print()
s.push(-1)
s.push(-9)
s.push(-4)
s.complete()
