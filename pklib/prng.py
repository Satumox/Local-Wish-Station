#!/usr/bin/env python3

class PRNG:
    def __init__(self, seed):
        self.seed = seed

    def rand(self):
        self.seed = (0x41C64E6D * self.seed + 0x6073) & 0xFFFFFFFF
        return self.seed
    
    