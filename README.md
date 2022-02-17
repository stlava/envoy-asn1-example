# Envoy Lua ASN.1 Example

This is an example of how to validate a request based on an ECDSA ASN.1 signature in Envoy’s lua engine. Please note this is only an example and is missing additional checks on the token that you might want in a production environment.

Starting server:
```
$ docker run -p 18000:18000 --mount type=bind,source="$(pwd)"/envoy-config,target=/envoy-config,readonly -it envoyproxy/envoy:v1.21.0 --config-path /envoy-config/envoy.yaml

[2022-02-17 22:19:44.229][29][info][lua] [source/extensions/filters/http/lua/lua_filter.cc:796] script log: filter beginning
[2022-02-17 22:19:44.230][29][info][lua] [source/extensions/filters/http/lua/lua_filter.cc:796] script log: x-amzn-oidc-data: eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiMTIzNCIsICJzaWduZXIiOiAiYXJuOmF3czplbGFzdGljbG9hZGJhbGFuY2luZzp1cy1lYXN0LTI6MTIzNDU2Nzg5MDpsb2FkYmFsYW5jZXIvYXBwL2Zvb2JhciJ9.eyJzdWIiOiAiMTIzNDU2Nzg5MCIsICJuYW1lIjogIlNsYXZhIiwgImVtYWlsIjogInNsYXZhQGV4YW1wbGUuY29tIn0=.quspn70308gCjLs3slvbuH5svek1wDBoeasFexzcrHPe_eFajgSt4x4q06IdgsYvKkxaT2WQiOOSber_2KGJxg==
[2022-02-17 22:19:44.230][29][info][lua] [source/extensions/filters/http/lua/lua_filter.cc:796] script log: checking signature against key
[2022-02-17 22:19:44.230][29][info][lua] [source/extensions/filters/http/lua/lua_filter.cc:796] script log: signature valid
```

Running the client:
```
$ pip install -r requirements.txt
$ python client.py

public key =
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmyuuRixAItd2StXgNOv7qfc/rMs1
dqLR7jaF3D+hEt/l9RPjsfqOFHwrOzOl6QpdoCVAPszYPocHp5FaI59ByQ==
-----END PUBLIC KEY-----

request headers: {'x-amzn-oidc-data': 'eyJhbGciOiAiRVMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiMTIzNCIsICJzaWduZXIiOiAiYXJuOmF3czplbGFzdGljbG9hZGJhbGFuY2luZzp1cy1lYXN0LTI6MTIzNDU2Nzg5MDpsb2FkYmFsYW5jZXIvYXBwL2Zvb2JhciJ9.eyJzdWIiOiAiMTIzNDU2Nzg5MCIsICJuYW1lIjogIlNsYXZhIiwgImVtYWlsIjogInNsYXZhQGV4YW1wbGUuY29tIn0=.quspn70308gCjLs3slvbuH5svek1wDBoeasFexzcrHPe_eFajgSt4x4q06IdgsYvKkxaT2WQiOOSber_2KGJxg=='}
response: 200 signature valid
```