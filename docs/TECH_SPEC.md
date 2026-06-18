# TECH_SPEC.md

## Cloud‑Migrator – Technical Specification

---

## 1. Overview

**Cloud‑Migrator** is a SaaS platform that assists enterprises in planning, executing, and validating cloud migration projects. It translates high‑level business objectives into concrete technical roadmaps, automates migration tasks, and provides continuous monitoring and reporting.

The system is built on a modular, event‑driven architecture that allows rapid iteration, easy integration with third‑party services, and secure multi‑tenant operation.

---

## 2. Architecture

```
┌───────────────────────┐
│ 1. Front‑end (React)  │
└───────┬───────────────┘
        │ REST / GraphQL
        ▼
┌───────────────────────┐
│ 2. API Gateway (Kong) │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 3. Service Layer      │
│    • Auth Service     │
│    • Project Service  │
│    • Planner Service  │
│    • Executor Service │
│    • Report Service   │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 4. Data Layer        │
│    • PostgreSQL      │
│    • Redis (cache)   │
│    • MinIO (object)  │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 5. Event Bus (Kafka) │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 6. Workers (Celery)   │
│    • Migration Worker │
│    • Notification     │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 7. External Integrations│
│    • Cloud Providers   │
│    • CI/CD Pipelines   │
│    • Monitoring (Prometheus) │
└───────────────────────┘
```

### 2.1 Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Micro‑service** | Each domain (auth, planning, execution) runs in its own container. |
| **Event‑driven** | Migration steps are triggered by Kafka events, enabling retry and audit. |
| **Multi‑tenant** | Tenant isolation via schema‑per‑tenant in PostgreSQL and tenant‑aware APIs. |
| **Observability** | Distributed tracing (OpenTelemetry), metrics (Prometheus), logs (ELK). |
| **Security** | OAuth2 + JWT, RBAC, TLS everywhere, secrets in Vault. |

---

## 3. Components

| Component | Responsibility | Tech |
|-----------|----------------|------|
| **Front‑end** | UI/UX, dashboards, wizard | React 18, TypeScript, Vite, Ant Design |
| **API Gateway** | Request routing, rate limiting, auth | Kong 3.x, OpenAPI spec |
| **Auth Service** | User & tenant auth, SSO | Keycloak, OAuth2, JWT |
| **Project Service** | CRUD for migration projects | FastAPI, SQLAlchemy |
| **Planner Service** | Generates migration plans | Python, Pandas, custom rule engine |
| **Executor Service** | Orchestrates migration steps | Celery + Redis, Docker SDK |
| **Report Service** | Generates PDF/HTML reports | ReportLab, Jinja2 |
| **PostgreSQL** | Persistent storage | 15.x, logical replication |
| **Redis** | Cache, Celery broker | 7.x |
| **MinIO** | Object storage for artifacts | S3‑compatible API |
| **Kafka** | Event bus | Confluent Kafka 3.x |
| **Workers** | Background jobs | Celery workers in Docker |
| **Monitoring** | Metrics & alerts | Prometheus, Grafana |
| **Tracing** | Distributed tracing | OpenTelemetry, Jaeger |
| **CI/CD** | Build, test, deploy | GitHub Actions, Docker Compose |

---

## 4. Data Model

### 4.1 Core Entities

| Table | Columns | Notes |
|-------|---------|-------|
| `tenants` | `id`, `name`, `created_at` | One‑to‑many with users |
| `users` | `id`, `tenant_id`, `email`, `role`, `hashed_pw` | RBAC |
| `projects` | `id`, `tenant_id`, `name`, `description`, `status`, `created_at` | Status: `draft`, `planned`, `executing`, `completed`, `failed` |
| `migration_steps` | `id`, `project_id`, `step_type`, `config_json`, `status`, `started_at`, `finished_at` | `step_type`: e.g., `copy`, `transform`, `validate` |
| `reports` | `id`, `project_id`, `generated_at`, `file_path` | Stored in MinIO |
| `audit_logs` | `id`, `tenant_id`, `user_id`, `action`, `details`, `timestamp` | Immutable |

### 4.2 Relationships

* One tenant → many users, projects, audit logs.
* One project → many migration steps, reports.
* Migration steps are processed sequentially but can be parallelized per project.

---

## 5. Key APIs / Interfaces

All APIs are versioned (`/api/v1/...`) and documented via OpenAPI 3.0.

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/auth/login` | POST | OAuth2 password grant | Public |
| `/projects` | GET, POST | List / create projects | Tenant‑scoped |
| `/projects/{id}` | GET, PATCH, DELETE | Retrieve / update / delete | Tenant‑scoped |
| `/projects/{id}/plan` | POST | Generate migration plan | Tenant‑scoped |
| `/projects/{id}/execute` | POST | Start execution | Tenant‑scoped |
| `/projects/{id}/steps` | GET | List steps | Tenant‑scoped |
| `/reports/{id}` | GET | Download report | Tenant‑scoped |
| `/metrics` | GET | Prometheus scrape | Service account |

### 5.1 Event Schema (Kafka)

| Topic | Event | Payload |
|-------|-------|---------|
| `migration.project.created` | Project created | `{project_id, tenant_id}` |
| `migration.plan.generated` | Plan ready | `{project_id, steps}` |
| `migration.step.started` | Step started | `{step_id, status}` |
| `migration.step.completed` | Step finished | `{step_id, status, metrics}` |
| `migration.project.completed` | Project finished | `{project_id, status}` |

---

## 6. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Front‑end** | React 18, TypeScript, Vite | Modern, fast, type safety |
| **API Gateway** | Kong | Open‑source, plugin ecosystem |
| **Auth** | Keycloak | SSO, fine‑grained roles |
| **Back‑end** | FastAPI | Async, auto‑docs, low latency |
| **Database** | PostgreSQL 15 | ACID, JSONB for configs |
| **Cache / Broker** | Redis 7 | Fast, supports pub/sub |
| **Object Store** | MinIO | S3 API, local dev |
| **Event Bus** | Confluent Kafka 3 | Durable, scalable |
| **Workers** | Celery 5, Docker SDK | Background tasks, retries |
| **Observability** | OpenTelemetry, Jaeger, Prometheus, Grafana | Full stack monitoring |
| **CI/CD** | GitHub Actions, Docker Compose | Rapid iteration |
| **Infrastructure** | Docker, Kubernetes (optional) | Containerized, scalable |

---

## 7. Deployment

### 7.1 Local Development

```bash
# Clone repo
git clone https://github.com/arkashira/cloud-migrator.git
cd cloud-migrator

# Start services
docker compose up -d

# Run migrations
docker compose exec api alembic upgrade head

# Seed demo data
docker compose exec api python scripts/seed_demo.py
```

### 7.2 Production

1. **Infrastructure** – Deploy to a managed Kubernetes cluster (EKS/GKE/Azure AKS) or ECS/Fargate.
2. **Secrets** – Store in Vault or KMS; mount as env vars.
3. **Database** – Provision a managed PostgreSQL cluster (RDS/CloudSQL) with read replicas.
4. **Kafka** – Use Confluent Cloud or self‑hosted cluster with TLS.
5. **MinIO** – Deploy as a stateful set or use S3.
6. **Ingress** – Kong Ingress Controller with TLS termination.
7. **Observability** – Prometheus Operator, Grafana, Jaeger.
8. **CI/CD** – GitHub Actions push to Docker registry, Helm chart deploy.

### 7.3 Scaling

| Service | Horizontal | Vertical |
|---------|------------|----------|
| API | Scale pods by request load | Increase CPU/RAM |
| Workers | Scale Celery workers | Increase concurrency |
| DB | Read replicas | Upgrade instance |
| Kafka | Add brokers | Increase broker resources |

---

## 8. Security

| Area | Measures |
|------|----------|
| **Transport** | TLS everywhere, mutual TLS for internal services |
| **Auth** | OAuth2 + JWT, Keycloak, 2FA |
| **RBAC** | Tenant‑scoped roles (`admin`, `planner`, `executor`) |
| **Secrets** | Vault/KMS, never in code |
| **Audit** | Immutable audit logs, signed |
| **Data** | Encryption at rest (PostgreSQL pgcrypto, MinIO) |
| **Network** | VPC isolation, security groups, private endpoints |

---

## 9. Testing

| Type | Tool | Coverage |
|------|------|----------|
| Unit | PyTest | 90%+ |
| Integration | Testcontainers (PostgreSQL, Kafka) | 80%+ |
| End‑to‑End | Cypress | UI flows |
| Load | k6 | API throughput |
| Security | OWASP ZAP | Vulnerability scan |

---

## 10. Roadmap (High‑Level)

1. **MVP (Q3 2026)** – Core planning, execution, reporting.
2. **Multi‑cloud support** – AWS, GCP, Azure connectors.
3. **AI‑assisted planning** – Use internal LLM for recommendation.
4. **Marketplace** – Third‑party migration scripts.
5. **Enterprise features** – SAML, custom branding.

---

## 11. Dependencies

| Package | Version | Notes |
|---------|---------|-------|
| FastAPI | ^0.95.0 | |
| SQLAlchemy | ^1.4.0 | |
| Alembic | ^1.8.0 | |
| Celery | ^5.2.0 | |
| Redis | ^4.0.0 | |
| Kafka-Python | ^2.8.0 | |
| MinIO Python SDK | ^7.0.0 | |
| OpenTelemetry | ^1.0.0 | |
| Kong | 3.x | |
| Keycloak | 21.x | |
| React | 18.x | |
| TypeScript | 4.x | |
| Vite | 4.x | |
| Ant Design | 5.x | |

All dependencies are pinned in `requirements.txt` / `pyproject.toml` and `package.json`. The Dockerfile uses multi‑stage builds to keep images lightweight.

---

## 12. Documentation

* **API Docs** – Auto‑generated Swagger UI at `/docs`.
* **Developer Guide** – `docs/developer.md`.
* **User Manual** – `docs/user.md`.
* **Contribution Guidelines** – `CONTRIBUTING.md`.

---

### Appendix

* **Data Flow Diagram** – See `docs/diagrams/data_flow.png`.
* **Sequence Diagram** – See `docs/diagrams/migration_sequence.png`.

---
