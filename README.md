# Field Calculator

Create a distribution of charged particles with optional labels.
Calculate the electric field at any position based on the distribution.
Or, calculate the electric force acting on one of the labeled charges in the distribution.

## Example

```py
>>> d = 0.200
>>> particles = [
...     Particle(-d, d, 512e-6, 1),
...     Particle(d, d, -427e-6, 2),
...     Particle(d, 0, 342e-6, 3),
...     Particle(0, -d, -179e-6, 4),
... ]
>>> dist = Distribution(particles)
>>> dist
Distribution([Particle(x=-0.2, y=0.2, q=0.000512, label=1), Particle(x=0.2, y=0.2, q=-0.000427, label=2), Particle(x=0.2, y=0, q=0.000342, label=3), Particle(x=0, y=-0.2, q=-0.000179, label=4)])
>>>
>>> dist.E(0, 0)
(-2250504.0608478636, -46984445.58554623)
>>> dist.F(1)
(7086.297951001512, -164.67764115638732)
```
