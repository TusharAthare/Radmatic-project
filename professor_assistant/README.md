# Professor Assistant AI

A Django-based AI assistant that helps professors manage student data using natural language processing through LangChain.

## Features

- Process natural language instructions for student data management
- Add new students to the database
- Record student scores
- Query student subjects
- Summarize student performance
- RESTful API interface
- Docker support

## Prerequisites

- Python 3.9+
- PostgreSQL
- Docker (optional)
- OpenAI API key

## Installation

### Local Setup

1. Clone the repository: 
```bash
git clone https://github.com/your-username/professor-assistant.git
cd professor-assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the server:
```bash
python manage.py runserver
```

### Docker Setup

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

## API Usage

### Process Instructions

POST `/api/process-instruction/`

Example requests:

1. Add a new student:
```json
{
    "instruction": "Add a new student named John Smith with ID 1234"
}
```

2. Add a score:
```json
{
    "instruction": "Add a score of 90 for Jane Doe in Math"
}
```

3. Query subject:
```json
{
    "instruction": "What subject did John Smith take?"
}
```

4. Summarize scores:
```json
{
    "instruction": "Summarize all student scores in Physics"
}
```

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
professor_assistant/
├── core/                  # Project settings
├── assistant/            # Main application
│   ├── migrations/      # Database migrations
│   ├── tests/          # Test cases
│   ├── models.py       # Database models
│   ├── serializers.py  # API serializers
│   ├── views.py        # API views
│   └── ai_helper.py    # LangChain integration
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── requirements.txt    # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

