#!/usr/bin/env python3
import struct
import argparse
from pathlib import Path
from pklib.prng import PRNG


# Mapping between Shift Value -> Inverse
# A = 0, B = 1, C= 2, D = 3
shiftMapInverse = shiftMapInverse = [
    [0, 1, 2, 3],
    [0, 1, 3, 2],
    [0, 2, 1, 3],
    [0, 3, 1, 2],
    [0, 2, 3, 1],
    [0, 3, 2, 1],
    [1, 0, 2, 3],
    [1, 0, 3, 2],
    [2, 0, 1, 3],
    [3, 0, 1, 2],
    [2, 0, 3, 1],
    [3, 0, 2, 1],
    [1, 2, 0, 3],
    [1, 3, 0, 2],
    [2, 1, 0, 3],
    [3, 1, 0, 2],
    [2, 3, 0, 1],
    [3, 2, 0, 1],
    [1, 2, 3, 0],
    [1, 3, 2, 0],
    [2, 1, 3, 0],
    [3, 1, 2, 0],
    [2, 3, 1, 0],
    [3, 2, 1, 0],
]

def gen5_decrypt(enc_data : bytes):

    if len(enc_data) not in [136, 220]:
        print('error')
        return
    
    region_0 = enc_data[:0x08]
    pid, _ , checksum = struct.unpack('IHH', enc_data[:0x08])

    # add data to Pokémon
    pkmn = region_0

    data = list(struct.unpack('H' * 64, enc_data[0x8:0x88]))
    prng = PRNG(checksum)

    # encrypting data
    for idx, Y in enumerate(data):
        data[idx] = (Y ^ (prng.rand() >> 16))

    # shuffle blocks
    shiftIdx = ((pid & 0x3E00) >> 0xD) % 24
    shiftOrder = shiftMapInverse[shiftIdx]

    region_1 = []
    for shuffle in shiftOrder:
        region_1 += data[16*shuffle:16*shuffle+16]

    region_1 = struct.pack('H' * 64, *region_1)

    # add data to Pokémon
    pkmn += region_1

    # decrypting battle stats
    if len(enc_data) == 220:
        data = list(struct.unpack('H' * int(len(enc_data[0x88:])/2), enc_data[0x88:]))

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
        enc_data = inputFile.read()
        dec_data = gen5_decrypt(enc_data)
        outputFile = open(filePath.name + ".dec", 'w+b')
        outputFile.write(dec_data)

        inputFile.close()
        outputFile.close()

    except OSError as err:
        print(f'{type(err)}:{err}')
    except Exception as err:
        print(f'Unexpected {err=}, {type(err)=}')
        raise
    