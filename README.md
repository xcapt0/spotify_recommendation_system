# 💃 Spotify recommendation system

Spotify recommendations are for you! Just choose the song you like and get your own recommendations

![giphy](https://user-images.githubusercontent.com/70326958/151396229-0763c23b-4cc6-4cb5-9832-bed006efb2cf.gif)

## 🛠️ Installation

```sh
git pull https://github.com/xcapt0/spotify_recommendation_system.git
docker build -t spotify .
```

## 🔍 Tests

Run tests with the following command:

```sh
python tests/test_spotify.py
```

## 👨‍💻 Usage

**Note**
> To use the app, you need to get `client_id`, `client_secret` and `refresh_token`.
> 1. Log in and create an application https://developer.spotify.com/dashboard/login
> 2. Get the `client_id` and `client_secret`
> 3. Follow the instructions https://developer.spotify.com/documentation/general/guides/authorization/code-flow/ to authorize your app
> 4. Paste `client_id`, `client_secret` and `refresh_token` into `config.yml` file

To run an app paste the follow command:

```sh
docker run --rm -p 5000:5000 -d spotify
```

## 📝 License

Copyright © 2022 [xcapt0](https://github.com/xcapt0).<br />
This project is [MIT](https://github.com/xcapt0/spotify_recommendation_system/blob/main/LICENSE) licensed.
