
# Proxy Venomizer

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Last commit](https://img.shields.io/github/last-commit/CookItUpProject/api-server)](https://img.shields.io/github/last-commit/CookItUpProject/proxy-venomizer)

ProxyVenomizer is a server proxy designed to intercept network traffic for seamless test scenario generation. This powerful tool acts as an intermediary, allowing users to craft and deploy custom testing scenarios by intercepting requests and responses.

## Installation

Create a Virtual Environment:

``` bash
virtualenv .venv
```

Activate the Virtual Environment:

``` bash
source .venv/bin/activate
```

Install Dependencies:

``` bash
pip install -r requirements.txt
```

## Usage

- Ensure the ProxyVenomizer server is running:

    ``` bash
    python3 app.py
    ```

- Make requests to external APIs by appending the API endpoint to the local server URL:

    ``` bash
    http://localhost:9797/https://pokeapi.co/api/v2/language
    ```

- Monitor the server console for logs.

- After stopping the program with `Ctrl + C`, inspect the generated tests.

## Related

Here are some related projects

- [Venom](https://github.com/ovh/venom)
## License

See the [LICENSE.md](LICENSE.md) file for details.