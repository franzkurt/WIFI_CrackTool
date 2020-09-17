# wpacrack

Reimplementing Aircrack-ng for didadic purposes.

The script follow the steps bellow:
  1. Sniff a WLAN to obtain a Handshake, similar to wireshark.
  2. Decode the packet to obtain MIC and information about the 802.x Auth protocol
  3. Generate with HMAC-SHA1 the possible values to PMK, PTK and compare with the original MIC.
  4. TO DO: Implement deauth packets to obtain a handshake in stealth mode
  
 
To run the script:
install dependencies:

  sudo pip install scapy hmac binascii ..
  
Run the script
   
  sudo python wpacrack.py
  
 
Link to file desciption of 802.x Auth stored at IPFS Gateway.

[a link](https://github.com/user/repo/blob/branch/other_file.md)

Thx for reading.
