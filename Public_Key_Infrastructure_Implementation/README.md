# Public Key Infrastructure Implementation

### 🛠️ Key Skills Demonstrated
![OpenSSL](https://img.shields.io/badge/OpenSSL-721412?style=for-the-badge&logo=openssl&logoColor=white)
![PKI](https://img.shields.io/badge/Public_Key_Infrastructure-blueviolet?style=for-the-badge)
![Security](https://img.shields.io/badge/X.509_Certificates-red?style=for-the-badge)
![Cryptography](https://img.shields.io/badge/RSA_2048-orange?style=for-the-badge)
![Networking](https://img.shields.io/badge/TLS-success?style=for-the-badge)

## 📖 Description:
Implemented a 3-tier Certificate Authority (CA) chain using OpenSSL, configuring a self-signed Root CA to sign Intermediate and End Entity
certificates for secure enterprise identity management.

I created a 3 level certificate chain using the below OpenSSL commands. It consisted of the Root CA – Golden Retriever Security, Intermediate CA – Corgi Certification Authority and the End Certificate – Shiba Inu Retail.

These are the commands I ran:

These commands were to create the root CA:
openssl genrsa -out root.key 2048
openssl req -x509 -new -sha256 -days 3650 -key root.key -out root.crt \
-subj "/C=AU/O=Golden Retriever Security/CN=530316273-Root" -extensions v3_ca -extfile root.cnf

These commands were to create the intermediate CA:
openssl genrsa -out inter.key 2048
openssl req -new -sha256 -key inter.key -out inter.csr \
-subj "/C=AU/O=Corgi Certification Authority/CN=530316273-Intermediate" openssl x509 -req -in inter.csr -CA root.crt -CAkey root.key -CAcreateserial \
-out inter.crt -days 1825 -sha256 -extensions v3_intermediate_ca -extfile inter.cnf 

These commands were to create the end CA:
openssl genrsa -out end.key 2048
openssl req -new -sha256 -key end.key -out end.csr \
-subj "/C=AU/O=Shiba Inu Retail/CN=530316273-End"
openssl x509 -req -in end.csr -CA inter.crt -CAkey inter.key -CAcreateserial \ -out end.crt -days 825 -sha256 -extensions usr_cert -extfile end.cnf

This command was to combine everything together and put it into full-cert-chain.pem cat end.crt inter.crt root.crt > full-cert-chain.pem