```markdown
# tech-spec.md

## 1. Stack

| Layer | Technology | Reasoning |
|-------|------------|-----------|
| **Backend** | **Go 1.22** (REST + gRPC) | Fast, compiled binaries, strong typing, excellent concurrency for migration orchestration. |
| **Web Framework** | **Gin** | Minimalistic, high‑performance, built‑in middleware for auth, logging, and metrics. |
| **Task Queue** | **Temporal.io** (Go SDK) | Durable, stateful workflow engine for long‑running migration jobs. |
| **Database** | **PostgreSQL 16** | ACID compliance, JSONB for flexible config, strong community. |
| **Cache** | **Redis 7** | Session store, rate limiting, job deduplication. |
| **Messaging** | **NATS JetStream** | Lightweight pub/sub for inter‑service communication. |
| **Frontend** | **React 18** + **TypeScript** | Rich UI for migration planning, visual workflow editor. |
| **Container Runtime** | **Docker 27** | Standard containerization for CI/CD and cloud deployment. |
| **Orchestration** | **Kubernetes 1.30** | Self‑hosted or managed (EKS/GKE/Azure AKS). |
| **Observability** | **Prometheus + Grafana**, **Jaeger**, **Loki** | Metrics, traces, logs. |

> **Why Go?** The migration engine is CPU‑bound (data transformation, diffing). Go’s lightweight goroutines and static binaries keep memory footprint low and deployment simple.

## 2. Hosting

| Environment | Platform | Notes |
|-------------|----------|-------|
| **Local dev** | Docker Compose | `docker-compose.yml` spins up Postgres, Redis, NATS, Temporal, and the API. |
| **Staging** | **DigitalOcean App Platform** (free tier) | Auto‑scales, supports Docker images, provides free TLS. |
| **Production** | **AWS EKS** (free tier first 12 mo) | Managed Kubernetes, IAM integration, ECR for images. |
| **CI/CD** | **GitHub Actions** | Free for public repos; self‑hosted runner for private. |

> *Free‑tier‑first* strategy: start with DigitalOcean for quick MVP, migrate to EKS once traffic > 10k/month.

## 3. Data Model

| Table | Key Fields | Description |
|-------|------------|-------------|
| **projects** | `id (UUID PK)`, `name`, `owner_id`, `created_at`, `updated_at` | Top‑level migration project. |
| **business_objectives** | `id`, `project_id FK`, `description`, `priority`, `created_at` | Business goals to be translated. |
| **technical_requirements** | `id`, `project_id FK`, `service_name`, `region`, `config_json`, `created_at` | Generated technical specs. |
| **migrations** | `id`, `project_id FK`, `status (queued, running, failed, succeeded)`, `started_at`, `completed_at`, `error_msg` | Migration job metadata. |
| **migration_steps** | `id`, `migration_id FK`, `step_name`, `status`, `log_url`, `started_at`, `completed_at` | Individual orchestrated steps. |
| **audit_logs** | `id`, `user_id`, `action`, `payload_json`, `timestamp` | Immutable audit trail. |
| **users** | `id`, `email`, `hashed_pw`, `role (admin, user)`, `created_at` | Auth users. |
| **secrets** | `id`, `project_id FK`, `key`, `value (encrypted)`, `created_at` | Encrypted storage for cloud creds. |

> **Indexes**: `projects.owner_id`, `migrations.project_id`, `migration_steps.migration_id`.

## 4. API Surface

| Method | Path | Purpose |
|--------|------|---------|
| `POST /api/v1/projects` | Create new migration project |
| `GET /api/v1/projects/{id}` | Retrieve project details |
| `POST /api/v1/projects/{id}/objectives` | Add business objective |
| `GET /api/v1/projects/{id}/objectives` | List objectives |
| `POST /api/v1/projects/{id}/requirements` | Generate technical requirements |
| `GET /api/v1/projects/{id}/requirements` | Retrieve generated specs |
| `POST /api/v1/projects/{id}/migrate` | Kick off migration workflow |
| `GET /api/v1/migrations/{id}` | Migration status & logs |
| `GET /api/v1/migrations/{id}/steps` | Step‑level details |
| `DELETE /api/v1/projects/{id}` | Delete project (soft delete) |

> All endpoints are **JSON‑only**, **idempotent** where applicable, and return `422` for validation errors.

## 5. Security Model

| Layer | Mechanism | Details |
|-------|-----------|---------|
| **Auth** | **JWT (HS256)** | Signed with a rotating secret stored in AWS Secrets Manager. |
| **Authorization** | RBAC | `admin` can manage all projects; `user` limited to own projects. |
| **Secrets** | **AWS KMS** | Encrypt `secrets` table values; key rotation every 90 days. |
| **Network** | **VPC** | All services in private subnets; API exposed via ALB with TLS termination. |
| **Rate Limiting** | **Redis** | 100 req/min per IP, 1000 req/min per user. |
| **Audit** | **audit_logs** table | Immutable, signed hash of payload. |
| **Secrets in CI** | GitHub Secrets | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `KMS_KEY_ID`. |

## 6. Observability

| Type | Tool | Data |
|------|------|------|
| **Logs** | **Loki** | Structured logs from API, Temporal workers, and frontend. |
| **Metrics** | **Prometheus** | `http_requests_total`, `migration_duration_seconds`, `db_query_latency_seconds`. |
| **Traces** | **Jaeger** | Distributed tracing across API → Temporal → DB. |
| **Alerting** | **Grafana Alerting** | SLA breaches, migration failures > 5%. |
| **Health Checks** | `/healthz` | Exposes readiness/liveness probes. |

## 7. Build / CI

| Step | Tool | Description |
|------|------|-------------|
| **Lint** | `golangci-lint` | Enforce code style, detect bugs. |
| **Unit Tests** | `go test -cover` | 80%+ coverage target. |
| **Integration Tests** | Docker Compose | Spin up Postgres, Redis, NATS, Temporal. |
| **Static Analysis** | `gosec` | Detect security issues. |
| **Build** | `docker buildx` | Multi‑arch (`linux/amd64`, `linux/arm64`). |
| **Publish** | `docker push` to ECR | Tag `latest` and semver. |
| **Deploy** | `kubectl apply -f k8s/` | Helm chart for EKS. |
| **Rollback** | `kubectl rollout undo` | Automatic on failed deploy. |
| **Secrets** | GitHub Actions secrets | KMS key, ECR creds. |

> **CI Pipeline**: `push` → lint → tests → build → push → deploy to staging. `merge` → same + promotion to prod after manual approval.

---

**End of tech‑spec v1.**