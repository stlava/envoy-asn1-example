import base64
import hashlib
import json
import requests

from ecdsa import NIST256p, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain


###############################################################################
# Generate signing key
#
# Create a signing key from a known seed to make testing easier. The public
# key (aka verification key) is pasted into the envoy.yaml config.
###############################################################################

def make_key(key_seed: bytes):
    secexp = randrange_from_seed__trytryagain(key_seed, NIST256p.order)
    return SigningKey.from_secret_exponent(secexp, curve=NIST256p)


seed = b'00000000000000000000000000000001'
private_key = make_key(seed)
public_key_pem = private_key.verifying_key.to_pem().decode('utf8')

print(f'public key = \n{public_key_pem}')

###############################################################################
# Create and sign JWT
###############################################################################
header = {
    "alg": "ES256",
    "typ": "JWT",
    "kid": "1234",
    "signer": "arn:aws:elasticloadbalancing:us-east-2:1234567890:loadbalancer/app/foobar"
}

claims = {
    "sub": "1234567890",
    "name": "Slava",
    "email": "slava@example.com"
}

jwt = '{}.{}'.format(
    base64.standard_b64encode(json.dumps(header).encode('utf8')).decode('utf8'),
    base64.standard_b64encode(json.dumps(claims).encode('utf8')).decode('utf8')
)

signature = private_key.sign(jwt.encode('utf8'), hashfunc=hashlib.sha256)
signature = base64.urlsafe_b64encode(signature).decode('utf8')
jwt = f'{jwt}.{signature}'

###############################################################################
# Make request to Envoy
###############################################################################
headers = {
    'x-amzn-oidc-data': jwt
}

print(f'request headers: {headers}')
resp = requests.get(url='http://localhost:18000', headers=headers)

print(f'response: {resp.status_code} {resp.text}')
