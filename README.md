# Social Media Scheduler - Full Stack Application

This is a complete full-stack application for AI-powered social media scheduling, product customization, and analytics dashboard built with FastAPI, Next.js, MySQL, Redis, and Celery.

## Features

### Challenge 1: AI Agent with Social Posting & Scheduling ✅
- **Smart Post Scheduling**: Schedule posts across multiple social platforms (Twitter, LinkedIn, Facebook, Instagram)
- **AI-Powered Suggestions**: Get hashtag recommendations and optimal posting time suggestions
- **Image Upload**: Attach images to your social media posts
- **Background Processing**: Uses Celery for reliable post scheduling and publishing
- **Status Tracking**: Monitor your posts' status (draft, scheduled, published, failed)

### Challenge 2: Product Customization Preview ✅
- **Interactive Canvas**: Add custom text overlays to product images (t-shirts)
- **Real-time Preview**: See your design changes instantly
- **Drag & Drop**: Position text anywhere on the product
- **Customization Options**: Adjust text size, color, and positioning
- **Design Management**: Save and view your custom designs

### Challenge 3: Analytics Dashboard ✅
- **Performance Metrics**: Track published, scheduled, and failed posts
- **Interactive Charts**: Visual representation using Recharts (bar charts and pie charts)
- **AI Insights**: Generate AI-powered insights about your posting performance
- **Filtering Options**: Filter analytics by platform, date range, and user
- **Performance Tips**: Built-in recommendations for improving engagement

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migrations
- **MySQL**: Primary database
- **Redis**: Message broker and caching
- **Celery**: Distributed task queue for background jobs
- **Pydantic**: Data validation and serialization

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Composable charting library
- **React Hook Form**: Performant forms with easy validation
- **Zod**: TypeScript-first schema validation
- **Lucide React**: Beautiful & consistent icons

### DevOps & Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **MySQL 8.0**: Database container
- **Redis 7**: Cache and message broker container

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd social-media-scheduler
```

### 2. Start the Application
```bash
docker-compose up -d
```

This will start all services:
- **MySQL**: Database (port 3306)
- **Redis**: Message broker (port 6379)
- **Backend**: FastAPI server (port 8000)
- **Frontend**: Next.js app (port 3000)
- **Celery Worker**: Background task processor
- **Celery Beat**: Task scheduler

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Initialize Database (First Run)
The database will be automatically migrated when the backend container starts.

## Development Setup

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Posts
- `POST /api/v1/posts/submit-post` - Schedule a new post
- `GET /api/v1/posts/posts` - List all posts
- `GET /api/v1/posts/post/{id}` - Get post details
- `POST /api/v1/posts/suggest-hashtag` - Get AI hashtag suggestions
- `POST /api/v1/posts/suggest-best-time` - Get optimal posting time suggestions

### Analytics
- `GET /api/v1/analytics/analytics/posts/summary` - Get post statistics
- `GET /api/v1/analytics/analytics/ai-insight` - Get AI-generated insights

### Product Customization
- `POST /api/v1/product-customization/product-designs` - Create custom design
- `GET /api/v1/product-customization/product-designs` - List user's designs
- `GET /api/v1/product-customization/product-designs/{id}` - Get design details

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │    Database     │
│   (Next.js)     │◄──►│   (FastAPI)      │◄──►│    (MySQL)      │
│   Port 3000     │    │   Port 8000      │    │   Port 3306     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │     Redis       │
                       │   Port 6379     │
                       └────────┬────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Celery Workers      │
                    │  Background Tasks     │
                    └───────────────────────┘
```

## Key Features Implementation

### 1. Social Media Scheduling
- Form-based post creation with platform selection
- Image upload functionality
- AI-powered hashtag generation
- Background task processing via Celery
- Real-time status updates

### 2. Product Customizer
- HTML5 Canvas for interactive design
- Drag-and-drop text positioning
- Real-time preview updates
- Database persistence of designs

### 3. Analytics Dashboard
- Chart.js integration for data visualization
- Real-time metrics calculation
- AI insight generation
- Filtering and date range selection

## Environment Variables

### Backend (.env)
```
DB_HOST=mysql
DB_PORT=3306
DB_NAME=social_scheduler
DB_USER=scheduler_user
DB_PASSWORD=scheduler_password
DATABASE_URL=mysql+pymysql://scheduler_user:scheduler_password@mysql:3306/social_scheduler
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
REDIS_URL=redis://redis:6379/0
USE_DUMMY_AI_PROVIDER=True
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Docker Services

The application runs in multiple Docker containers:

1. **mysql**: Database service
2. **redis**: Message broker and cache
3. **backend**: FastAPI application server
4. **celery-worker**: Background task processor
5. **celery-beat**: Task scheduler
6. **frontend**: Next.js web application

## Development Notes

- The backend uses mock AI providers for development (set `USE_DUMMY_AI_PROVIDER=True`)
- Database migrations run automatically on backend startup
- The frontend includes responsive design for mobile and desktop
- Error handling and loading states are implemented throughout
- TypeScript ensures type safety across the frontend

## Production Considerations

- Replace dummy AI providers with real API keys
- Configure proper database backups
- Set up monitoring and logging
- Use environment-specific Docker configurations
- Implement proper security headers and CORS policies
- Set up SSL/TLS certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for interview/demonstration purposes.