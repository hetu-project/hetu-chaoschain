# Proposal Agent API Service

An intelligent proposal generation and management service built on FastAPI, integrating OpenAI language models for automated proposal processing.

![API Service](assets/summary-view.jpg)

## Features

- 🚀 Intelligent proposal generation based on OpenAI models
- 🔗 LangChain-driven semantic parsing and processing
- ⚡ Real-time API endpoints for quick integration
- � Secure environment variable configuration management
- � Built-in debug mode and multi-level logging system

## Requirements

- Python 3.9+
- OpenAI API key
- pip 20.0+

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment
Copy the example environment file and configure parameters:
```bash
cp .env.example .env
```
Edit `.env` file configuration:
```ini
OPENAI_API_KEY=sk-your-key-here  # Required
BASE_URL=https://your.proxy.com/v1  # Custom API endpoint
```

### Start Service
```bash
python main.py
```
Service runs by default at: `http://0.0.0.0:8000`

## API Documentation

Access local Swagger documentation at:
`http://localhost:8000/docs`

### Core Endpoints
- `POST /api/proposals` Create new proposal
- `GET /api/proposals/{id}` Get proposal details
- `PUT /api/proposals/{id}` Update proposal status

## Development Configuration

| Environment Variable | Default Value | Description                    |
|---------------------|---------------|--------------------------------|
| DEBUG               | True          | Enable hot reload and debug mode|
| LOG_LEVEL           | INFO          | Log level (DEBUG/INFO/WARN)    |
| API_HOST            | 0.0.0.0       | Service binding address        |
| API_PORT            | 8000          | Service listening port         |

## Contribution Guide
1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push branch (`git push origin feature/NewFeature`)
5. Create Pull Request

## License
[MIT License](LICENSE)
