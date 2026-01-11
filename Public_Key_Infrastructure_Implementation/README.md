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