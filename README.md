# Testing remote services with vcr and respx

This is an example case for my blog post about [testing remote services on httpx and respx and vcr](http://rogulski.it/blog/pytest-httpx-vcr-respx-remote-service-tests/) 

## Install requirements

```bash
pip-compile --generate-hashes --output-file=requirements.txt requirements.in
```


## Run tests
```bash
pytest tests
```
