#!/usr/bin/env python3
import struct
import argparse
from pathlib import Path
from pklib.prng import PRNG

# Mapping between Shift Value -> Block Order
# A = 0, B = 1, C= 2, D = 3
shiftMap = [
    [0, 1, 2, 3],
    [0, 1, 3, 2],
    [0, 2, 1, 3],
    [0, 2, 3, 1],
    [0, 3, 1, 2],
    [0, 3, 2, 1],
    [1, 0, 2, 3],
    [1, 0, 3, 2],
    [1, 2, 0, 3],
    [1, 2, 3, 0],
    [1, 3, 0, 2],
    [1, 3, 2, 0],
    [2, 0, 1, 3],
    [2, 0, 3, 1],
    [2, 1, 0, 3],
    [2, 1, 3, 0],
    [2, 3, 0, 1],
    [2, 3, 1, 0],
    [3, 0, 1, 2],
    [3, 0, 2, 1],
    [3, 1, 0, 2],
    [3, 1, 2, 0],
    [3, 2, 0, 1],
    [3, 2, 1, 0],
]

def gen5_encrypt(dec_data : bytearray):

    if len(dec_data) not in [136, 220]:
        print('error')
        return
    
    region_0 = dec_data[:0x08]
    pid, _ , checksum = struct.unpack('IHH', dec_data[:0x08])

    # add data to Pokémon
    pkmn = region_0

    data = list(struct.unpack('H' * 64, dec_data[0x8:0x88]))
    prng = PRNG(checksum)

    # unshuffle blocks
    shiftIdx = ((pid & 0x3E00) >> 0xD) % 24
    shiftOrder = shiftMap[shiftIdx]

    region_1 = []
    for shuffle in shiftOrder:
        region_1 += data[16*shuffle:16*shuffle+16]

    # decrypt data
    for idx, Y in enumerate(data):
        data[idx] = (Y ^ (prng.rand() >> 16))

    region_1 = struct.pack('H' * 64, *region_1)

    #add data to Pokémon
    pkmn += region_1

    # encrypting battle stats
    if len(dec_data) == 220:
        data = list(struct.unpack('H' * int(len(dec_data[0x88:])/2), dec_data[0x88:]))

        prng = PRNG(pid)
        for idx, Y in enumerate(data):
            data[idx] = (Y ^ (prng.rand() >> 16))

        region_2 = struct.pack('H' * 42, *data)

        # add data to Pokémon
        pkmn += region_2

    return pkmn

if __name__ == '__main__':
    parser = argparse.ArgumentParser('PK5 Decrypter', 'decrypt.py <pkmn.pk5>', 'Decyrption tool for .pk5 files.')
    parser.add_argument('pk5_file', metavar='pkmn.pk5', type=Path, help='.pk5 file to decrypt')

    args = parser.parse_args()

    filePath : Path = args.pk5_file

    try:
        inputFile = filePath.open('r+b')
        dec_data = inputFile.read()
        enc_data = gen5_encrypt(dec_data)
        outputFile = open(filePath.name + ".enc", 'w+b')
        outputFile.write(enc_data)

        inputFile.close()
        outputFile.close()

    except OSError as err:
        print(f'{type(err)}:{err}')
    except Exception as err:
        print(f'Unexpected {err=}, {type(err)=}')
        raise