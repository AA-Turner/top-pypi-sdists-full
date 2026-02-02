import rx
from rx import operators as op


def inspect(x):
    print(f"fuck {x}")
    return x


def multi():
    def go(source):
        observers = []

        def on_next(value):
            for obv in observers:
                obv.on_next(value)

        def on_error(value):
            for obv in observers:
                obv.on_error(value)

        def on_completed():
            for obv in observers:
                obv.on_completed()

        def subscribe(obv, scheduler):
            observers.append(obv)
            return dispo

        dispo = source.subscribe_(on_next, on_error, on_completed)
        return rx.Observable(subscribe)

    return go


m = rx.of(1, 2, 3)
m = m.pipe(op.map(inspect))
# m = m.pipe(multi())
# m = m.pipe(op.multicast(subject_factory=lambda _: rx.subject.ReplaySubject(), mapper=lambda x:x))
m = m.pipe(op.multicast(subject=rx.subject.Subject(), mapper=lambda x: x))
# m = m.pipe(op.multicast())

print("subscribing shit")
m.subscribe(print)
m.subscribe(print)
m.subscribe(print)
