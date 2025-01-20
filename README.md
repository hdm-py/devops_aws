# Project Title

**System Monitoring and API Project**

## Overview
This project includes a FastAPI application alongside a system health monitoring tool. The system tracks CPU, memory, disk usage, and SSH attempts, sending alerts to a Discord webhook when thresholds are exceeded.

## Features

1. **FastAPI Application**:
    - A simple web API that responds to GET requests at `/` with a "Hello World" message.

2. **System Health Monitoring**:
    - Monitors CPU, memory, and disk usage.
    - Tracks failed SSH login attempts.
    - Sends real-time alerts to a Discord webhook.

3. **Docker Integration**:
    - Fully containerized using Docker and Docker Compose.

4. **Backup Automation**:
    - A bash script to automate database backups.

## Project Structure

```
.
├── app.py                 # FastAPI application
├── health_monitor.py      # System health monitoring script
├── backup.sh              # Database backup script
├── setup.sh               # Initial setup script
├── supervisord.conf       # Supervisor configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
└── crontab                # Cron job configuration for periodic tasks
```

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher
- Git

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Run Setup Script**:
   ```bash
   ./setup.sh
   ```

3. **Build and Start Services**:
   ```bash
   docker-compose up --build
   ```

4. **Access FastAPI**:
   Open your browser and navigate to `http://localhost:8000`.

## Usage

### FastAPI

- Endpoint: `/`
- Method: `GET`
- Response:
  ```json
  {
    "message": "Hello World"
  }
  ```

### System Health Monitoring

- Starts automatically with Supervisor.
- Alerts are sent to the configured Discord webhook.

### Backup Automation

- Executes periodically via cron.
- Backup files are saved in the `./backups` directory.

## Configuration

### Environment Variables

- Configure the Discord webhook URL and other environment variables in a `.env` file.

Example `.env` file:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### Supervisor

- Configuration for Supervisor is provided in `supervisord.conf`.

## Dependencies

Install dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Contributing

Feel free to fork this repository and submit pull requests. Ensure code quality by following PEP 8 guidelines.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Happy Coding!

