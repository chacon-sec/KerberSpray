# KerberSpray
A Python-based Kerberos password spraying tool that wraps [`impacket-getTGT`](https://github.com/SecureAuthCorp/impacket) to check for valid user/password combinations against a Windows Domain Controller. Supports a user file, password file, logs outputs, and .ccache ticket generation. This has been done before, and probably better just wanted to whip something up for a htb challenge I was doing.

## 🧰 Requirements
- Python 3.x
- [Impacket](https://github.com/SecureAuthCorp/impacket)

## ⚙️ Usage

```bash
python3 kerberos_spray.py \
  -d example.com \
  --dc-ip 192.168.1.1 \
  -u users.txt \
  -p passwords.txt \
  -o valid_creds.txt