k = 8.99e+9

class Particle:
    def __init__(self, x: float, y: float, z: float, q: float, label: int|str = None) -> None:
        """
        Create a new particle of charge q at position (x, y, z).
        """
        self.x = x
        self.y = y
        self.z = z
        self.q = q
        self.label = label

    def __repr__(self) -> str:
        return f"Particle(x={self.x}, y={self.y}, z={self.z}, q={self.q}, label={self.label})"

    @property
    def r(self) -> float:
        """
        Return the distance of the particle from the origin.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def E(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """
        Return the x, y, and z components of the electric field at the specified (x, y, z) position.
        """
        delta_x = x - self.x
        delta_y = y - self.y
        delta_z = z - self.z
        delta_r = (delta_x**2 + delta_y**2 + delta_z**2)**0.5
        E_mag = k * self.q / delta_r**2
        E_x = E_mag * (delta_x / delta_r)
        E_y = E_mag * (delta_y / delta_r)
        E_z = E_mag * (delta_z / delta_r)
        return (E_x, E_y, E_z)

    def V(self, x: float, y: float, z: float) -> float:
        """
        Return the electric potential at the specified (x, y, z) position.
        Assume V -> 0 as r -> inf.
        """
        delta_x = x - self.x
        delta_y = y - self.y
        delta_z = z - self.z
        delta_r = (delta_x**2 + delta_y**2 + delta_z**2)**0.5
        V = k * self.q / delta_r
        return V

class Distribution:
    def __init__(self, particles: list[Particle] = None) -> None:
        """
        Create a new particle distribution.
        """
        self.particles: list[Particle] = []
        if particles is not None:
            self.add_particles(particles)

    def __repr__(self) -> str:
        return f"Distribution({self.particles})"
    
    @property
    def labels(self) -> list[str]:
        """
        Return the list of non None particle labels in use.
        """
        return [item.label for item in self.particles if item.label is not None]

    def add_particle(self, particle: Particle) -> None:
        """
        Add a particle to the distribution.
        If the label is None, add it without issuse.
        If the label is not None, check that the label is not taken by another particle in the list.
        """
        if particle.label in self.labels:
            raise ValueError("Particle label already in use.")
        self.particles.append(particle)

    def add_particles(self, particles: list[Particle]):
        """
        Add the input list of particles to the distribution.
        """
        for particle in particles:
            self.add_particle(particle)

    def get_particle(self, label: int|str) -> Particle:
        """
        Get the particle with the given label.
        """
        if label in self.labels:
            for particle in self.particles:
                if label == particle.label:
                    return particle
        else:
            raise ValueError("Particle label not found.")

    def E(self, x: float, y: float, z: float, exclude: list[str] = None) -> tuple[float, float, float]:
        """
        Return the x, y, z components of the electric field at the specified (x, y, z) position.
        Exclude the particles with the specifiecd labels.
        """
        if exclude is None:
            exclude = []
        E_tot_x = 0.0
        E_tot_y = 0.0
        E_tot_z = 0.0
        for particle in self.particles:
            if particle.label in exclude:
                continue
            E_x, E_y, E_z = particle.E(x, y, z)
            E_tot_x += E_x
            E_tot_y += E_y
            E_tot_z += E_z
        return (E_tot_x, E_tot_y, E_tot_z)

    def V(self, x: float, y: float, z: float, exclude: list[str] = None) -> float:
        """
        Return the electric potential at the specified (x, y, z) position.
        Exclude the particles with the specifiecd labels.
        Assume V -> 0 as r -> inf.
        """
        if exclude is None:
            exclude = []
        V_tot = 0.0
        for particle in self.particles:
            if particle.label in exclude:
                continue
            V = particle.V(x, y, z)
            V_tot += V
        return V_tot

    def F(self, label: str) -> tuple[float, float, float]:
        """
        Return the x, y, z components of the electric force on the particle with the specified label.
        """
        particle = self.get_particle(label)
        x = particle.x
        y = particle.y
        z = particle.z
        q = particle.q
        E_x, E_y, E_z = self.E(x, y, z, exclude=[label])
        F_x = q * E_x
        F_y = q * E_y
        F_z = q * E_z
        return (F_x, F_y, F_z)
    
    def U(self) -> float:
        """
        Return the electric potential energy of the distribution of particles.
        Assume U -> 0 as r -> inf.
        """
        U_tot_double = 0
        particles = self.particles.copy()
        for particle in particles:
            q = particle.q
            x = particle.x
            y = particle.y
            z = particle.z
            self.particles.remove(particle)
            U = q * self.V(x, y, z)
            U_tot_double += U
            self.particles.append(particle)
        U_tot = U_tot_double / 2
        return U_tot
