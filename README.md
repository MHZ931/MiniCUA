# MiniCUA

A minimal Linux workshop based on Alpine that hosts a custom FastAPI-based endpoint that enables communication from computer using agents (CUAs).

This repository includes:

- A minimal image that includes basic functionalities (browser, terminal, VNC) and an API endpoint
- An MCP-server script that can be connected to the API endpoint

## Running the server

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