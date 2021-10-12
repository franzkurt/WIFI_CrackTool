## Crackeando a senha WPA2 de Redes WiFi com Scapy.py
Baseada na ferramenta de penetration test aircrack https://www.aircrack-ng.org/
:octocat:

### Documento explicando a construção da ferramenta para fins didáticos:
  - IPFS [Doc WPA2 - Authentication](https://gateway.pinata.cloud/ipfs/QmZwXohZ8yai8gwSjx2NLbfBCLKbbUGXTLehGrzSezdJqv)
  - Diretório github: /documento.pdf

## Fluxo :bomb:
  1. Procura em um arquivo .pcap ou escuta na rede por um handshake (Similar ao Airodump-ng)
  2. Enocntra as informações necessárias realizando um decode nos pacotes
  3. Gera através da função HMAC-SHA1 os possiveis valores de PMK, PTK e compara com o MIC obtido no handshake.
 
```
git clone https://github.com/franzkurt/WIFI_CrackTool.git
cd WIFI_CrackTool/
pip install scapy hmac binascii
python wpacrack.py (A interface de rede será resetada)
```

## Repositório
```
WiFi_CrackTool/
├─ wordlists/
│  ├─ rockyou.txt
│  ├─ passwords.txt
│  ├─ hashes.txt
├─ src/
   ├─ wpacrack.py

```
## TODO
- [x] Criar um script que escute os pacotes na rede em modo promiscuo
- [x] Filtrar apenas os pacotes de autenticação
- [x] Descobrir a senha traffegada por meio de quebra de criptografia (Rainbow Tables)
- [ ] Manipular pacotes em real-Time
- [ ] Implementar a desautenticação (similar ao airreplay-ng)

Thx for reading.
