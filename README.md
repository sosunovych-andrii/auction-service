# Auction Service

## ⚙️Tech-Stack
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker / Docker Compose
- Poetry

## 🚀Installation
1. **Clone the repository:**
```shell
   git clone https://github.com/sosunovych-andrii/auction-service.git
````
2. **Create a .env file in the root directory of the project** and copy the content from .env.sample:
```shell
  cp .env.sample .env
```
3. **Build and start containers:**
```shell
  docker-compose up --build
```
4. **Apply migrations**
```shell
   docker-compose exec app poetry run alembic upgrade head
```
5. **Open API documentation (Swagger UI) in your browser http://localhost:8000/docs/**
