import polytope


p = polytope.box2poly([[0, 1], [0, 1]])
q = polytope.box2poly([[0.5, 1.5], [0.5, 1.5]])
r = polytope.box2poly([[0.5, 1.5], [-0.5, 0.5]])
s = polytope.box2poly([[-0.5, 0.5], [-0.5, 0.5]])

# Check empty set-minus
assert not polytope.is_empty(polytope.mldivide(p, polytope.Region()))

# Check that single subtractions are nonempty
t = polytope.mldivide(p, q)
assert not polytope.is_empty(t)

u = polytope.mldivide(p, r)
assert not polytope.is_empty(u)

v = polytope.mldivide(p, s)
assert not polytope.is_empty(v)

# Check that subtraction of union of two polytopes is nonempty
qr = polytope.Region([q, r])
w = polytope.mldivide(p, qr)
assert not polytope.is_empty(w)

# Check that subtraction of union of three polytopes is nonempty
qrs = polytope.Region([q, r, s])
x = polytope.mldivide(p, qrs)
assert not polytope.is_empty(x)
