# Phone Inventory Backend

A REST API for tracking inventory at repair shops and resale stores. Helps owners record what they paid for each phone, its current condition,and the price the same model is going for in the market.

This project is being built as a hands-on learning vehicle for backend development and DevOps - flask, REST API design, SQL databases, Docker, CI/CD, and Cloud deployment.

## Tech Stack

- **Backend:** Python3 + Flask
- **Database:** SQLite (Will migrate to PostgreSQL)
- **Frontend (Planned):** React
- **Deployment (planned):** Docker on a self-hosted Linux server, eventually AWS

## Current Status

**Phase 1 — In progress:** Flask backend with in-memory data.

- [x] Project scaffolding with virtual environment
- [x] `GET /phones` endpoint returning hardcoded inventory
- [ ] `POST /phones` to add new phones
- [ ] `GET /phones/<id>` to fetch one phone
- [ ] `PUT` and `DELETE` endpoints
- [ ] Migrate from in-memory list to SQLite
- [ ] Input validation and proper error handling
- [ ] Dockerize and deploy to home server

## Running Locally

```bash
# Clone and enter the project
git clone https://github.com/patrickian2001-jpg/phone-inventory-backend.git
cd phone-inventory-backend

# Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install Flask

# Run the development server
flask --app app run
```

The server starts on `http://127.0.0.1:5000`.

## API Endpoints

| Method | Path      | Description           |
|--------|-----------|-----------------------|
| GET    | `/phones` | List all phones       |

## License

MIT (coming soon)
