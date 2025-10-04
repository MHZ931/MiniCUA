# MiniCUA

A minimal Linux workshop based on Alpine that hosts a custom FastAPI-based endpoint that enables communication from computer using agents (CUAs).

This repository includes:

- A minimal image that includes basic functionalities (browser, terminal, VNC) and an API endpoint
- An MCP-server script that can be connected to the API endpoint

## Building the image

To pull and run the image, simply run:

```shell
# Pull the image
docker pull mhz139/minicua

# Run the image
docker run --rm -p 5900:5900 -p 6080:6080 --hostname alpine mhz139/minicua
```

Since this is equipped with a VNC server, you can go to [localhost:6080](http://localhost:6080) to view the server.

In addition, if you have TigerVNC, you can use docker's default address with port 5900 to view it in TigerVNC.

## Running the server

Before running the server, make sure the image is built and run first.

To run the tools server, the simplest way is to install `uv` and then use `uvx` to run the server directly:
```shell
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the server
uvx minicua-mcp-server
```

Or you can add the server into your favorite LLM workflows:

```json
    "minicua-mcp-server": {
      "command": "uvx",
      "args": [
        "minicua-mcp-server"
      ]
    }
```

## Dependencies

- python >= 3.12
- fastmcp>=2.12.4
- pillow>=11.3.0

Special Thanks to [rwildcat/docker_alpine-vnc](https://github.com/rwildcat/docker_alpine-vnc) for offering an awesome barebone VNC connected Linux image to work with.