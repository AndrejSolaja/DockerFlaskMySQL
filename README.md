# DockerFlaskMySQL
Deploying a Python application leveraging Flask, Docker Compose, MySQL.

##Installation

Run following command in directory with docker-compose.yml file
```bash
docker-compose up --build
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requests.
```bash
pip install requests
```

##Usage

Run console.py
```bash
python console.py
```
By using simple menu-style app in console you can communicate with app by sending HTTP requests on localhost:5000 and directly change MySQL database.

