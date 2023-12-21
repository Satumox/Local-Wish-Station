# Local-Wish-Station
Local-Wish-Station is a program which allows you to clone your own Pokémon in generation 5 Games (B/W/B2/W2) through the GTS.

## Requirements
- Python 3.11+ 

## Instructions

### Step 1

```bash
$ git clone https://github.com/Satumox/Local-Wish-Station.git
$ cd Local-Wish-Station
$ python local-wish-station.py
```

### Step 2
On your game console, set the DNS server to the IP address that is mentioned in the output.

    Please set your DNS to 192.168.178.31 on your game console.
    Local Wish Station is running!
    Type in 'q' to quit
    >

### Step 3
Start your generation 5 game and enter the GTS to deposit the Pokémon you want to clone.
After trying to deposit a Pokémon  an error message should appear and throw the game back to the main menu of the GTS.
The script should print the message:

    Stored the data for cloning!
    Reenter the GTS to collect your clone.

### Step 4
Leave the GTS and reenter it, the game should receive the same Pokémon that you previously tried to deposit. Everytime the GTS is entered, the same Pokémon is sent. You can overwrite the data by trying to deposit a different Pokémon.


## Troubleshooting

The script will tell you the local IP address of the device on which the script is running, which needs to be set as DNS server on your console. Adding rules to your firewall for incoming traffic through port 53 and 80 might be necessary in order for the tool to function. On Unix-like systems, running the script with root privileges is necessary in order to use port 53 and 80.

## Credits
Thanks to evandixon for documenting the GTS protocol, BW PK5 Structure, PRNG in Pokémon and the list of Wi-Fi addresses.
- GTS Protocol: https://projectpokemon.org/home/docs/gen-5/gts-protocol-r19/
- BW PK5 Structure: https://projectpokemon.org/docs/gen-5/bw-save-structure-r60/
- PRNG in Pokémon: https://projectpokemon.org/home/docs/other/prng-in-pok%C3%A9mon-r38/
- List of Wi-Fi Addresses: https://projectpokemon.org/home/docs/other/list-of-wi-fi-addresses-r25/

Thanks to the Kaeru Team for enabling online play for DS and DSi games over Wiimmfi, without the need for patches.
- Kaeru Team: https://kaeru.world/

Thanks to Wiimm & Leseratte for providing free online play through their WFC replacement service called Wiimmfi.
- Wiimmfi: https://wiimmfi.de/
