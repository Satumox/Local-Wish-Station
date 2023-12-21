def add_gts_data(data : bytearray):
    data += b'\x00' * 16 # add 16 bytes padding
    data += data[0x08:0xA]  # National Pokédex ID
    data += data[0x40].to_bytes(length=1, byteorder='little')  # gender & alternate forms
    data += data[0x8C].to_bytes(length=1, byteorder='little')   # level
    data += b'\x01\00'  # requested Pokémon (Bulbasaur)
    data += b'\x03'     # requested gender (Either/neither)
    data += b'\x00'     # min level
    data += b'\x00'     # max level
    data += b'\x00'     # unknown
    data += b'\x00'     # Trainer gender(male)
    data += b'\x00'     # unknown
    data += b'\x07\xE7' # year deposited (2023)
    data += b'\x05'     # month deposited (May)
    data += b'\x07'     # day deposited (07)
    data += b'\x0D'     # hour (13)
    data += b'\x25'     # minutes (37)
    data += b'\x00'     # seconds (0)
    data += b'\x00'     # unknown
    data += b'\x07\xE7\x05\x07\x14\x0F\x00\x00' #2023-05-07 20:15:00 ?
    data += data[0x0:0x4]   # PID
    data += data[0xC:0xE]   # OT ID
    data += data[0xE:0x10]  # OT Secret ID
    data += data[0x68:0x78] # OT Name
    data += b'\xDB\x02' # country, city
    data += b'\x0C'     # Trainer's sprite (Researcher)
    data += b'\x01'     # exchanged flag
    data += b'\x15'     # Game version (Black)
    data += b'\x05'     # Language (German)
    data += b'\x01\x00' # unknown

    if len(data) != 296:
        print("Something is wrong my friend!")
        return None
    
    return data

