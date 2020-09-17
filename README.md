<h2 align="center"> Script to Crack WPA2 math Keys</h2> 
<p align="center">
  <img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
</p>
<ul>
  <li><b>Aircrack-ng: </b> <a href="https://www.aircrack-ng.org/" target="_blank">https://www.aircrack-ng.org/</a></li>
</ul>
# repository wpacrack

Reimplementing Aircrack-ng for didadic purpose.
Reimplementando o Aircrack-ng para estudos.

The script follow the steps bellow:
  1. Sniff a WLAN to obtain a Handshake, similar to airodump-ng.
  2. Decode the packet to obtain MIC and information about the 802.x Auth protocol
  3. Generate with HMAC-SHA1 the possible values to PMK, PTK and compare with the original MIC.
  4. TO DO: Implement deauth packets to obtain a handshake in stealth mode

O Script segue os passo abaixo:
  1. Procura em um arquivo .pcap ou escuta na rede por um handshake (Similar ao Airodump-ng)
  2. Enocntra as informações necessárias realizando um decode nos pacotes
  3. Gera através da função HMAC-SHA1 os possiveis valores de PMK, PTK e compara com o MIC obtido no handshake.
  4. FAZER: Implementar a desautenticação (similar ao airreplay-ng)

To run the script:
install dependencies:

  sudo pip install scapy hmac binascii ..
  
Run the script
   
  sudo python wpacrack.py
  
 
Link to file desciption of 802.x Auth stored at IPFS Gateway.

[Description AUTH - PDF](https://gateway.pinata.cloud/ipfs/QmZwXohZ8yai8gwSjx2NLbfBCLKbbUGXTLehGrzSezdJqv)

Thx for reading.
