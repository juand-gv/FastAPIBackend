# Project Notes

Project based on [Curso de PYTHON desde CERO para BACKEND  by MoureDev by Brais Moure](https://youtu.be/_y9qQZXE24A)

## FastAPI

[FastAPI Docs](https://fastapi.tiangolo.com/tutorial/)

**To start the uvicorn server:**

``` bash
uvicorn main:app --reload
```

* **--reload:** Reloads the server ecery single time you modify the main.yp file

* **"http://127.0.0.1:8000/docs":** Gets you the Swagger docs
* **"http://127.0.0.1:8000/redoc":** Gets you the Redocly docs

## MongoDB

[MongoDB Docs](https://www.ionos.com/digitalguide/websites/web-development/install-mongodb-ubuntu/)

**Start server:**

``` bash
sudo systemctl start mongod
```

**Check status:**

``` bash
sudo systemctl status mongod
```

**Stop server:**

``` bash
sudo systemctl stop mongod
```

## Atlas MongoBD

**DB Credentials:**

[Atlas url](https://cloud.mongodb.com/v2/641a3c888943eb5950976cbc#/clusters)

* Username: test
* Password: testpass

## Deploying on Deta.Space

**Installing Space CLI:**

```bash
curl -fsSL https://get.deta.dev/space-cli.sh | sh
```

**Access Token:**

Valid for 12 months:

5nV1rQgg_FWmfP8zc78zkY7zffmsYdWvfkHvzu68H

**Login:**

```bash
space login
```

**Creating Project:**

```bash
space new
```

**URL:**

[FasAPI Deploy Docs](https://fastapi.tiangolo.com/deployment/deta/)

[Deployment url](https://deta.space/builder/e0uWhvGYiLCX)

**Info about Auth:**

Deta Space provides auth with their own page, but since I already implemented jwt, I want the routes to be public.

[Deta Space Auth Docs](https://deta.space/docs/en/basics/micros#public-routes)

**Pushing changes:**

```bash
space push
```

**Releasing project:**

```bash
space release --listed
```
