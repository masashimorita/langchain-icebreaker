# LangChain Ice Breaker
Ice Breaker app created with LangChain.

![masacode_A_modern_minimalist_logo_of_brand_name_Ice_Breaker_Vec_128f947f-5423-45fb-9da3-96cd2d573355](https://github.com/user-attachments/assets/cac510d1-eeb6-48a8-8564-52df9027bc64)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```
OPENAI_API_KEY=
PROXYCURL_API_KEY=
TAVILY_API_KEY=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
```

## Run Application on Local

Clone the project

```bash
  git clone https://github.com/masashimorita/LangChainIceBreaker.git
```

Go to the project directory

```bash
  cd LangChainIceBreaker
```

Create Network

```bash
  docker network create ollama_default
```

Build Docker image

```bash
  docker compose build
```

Access Docker Image

```bash
  docker compose run --rm app bash
```

Install dependencies

```bash
  poetry install
```

Start the flask server

```bash
  docker compose up
```
