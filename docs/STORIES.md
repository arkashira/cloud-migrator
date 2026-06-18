# STORIES.md

## Cloud‑Migrator – User Story Backlog

> **Goal** – Deliver a minimum‑viable product that lets an enterprise architect plan, validate, and execute a cloud migration with confidence, while capturing business objectives and technical constraints.

---

## Epic 1 – Capture Business Objectives

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **1.1** | **As a** business stakeholder, **I want** to define high‑level migration goals (e.g., cost reduction, compliance, scalability) **so that** the migration plan aligns with corporate strategy. | • A form with fields: *Goal*, *Target KPI*, *Priority*, *Deadline*.<br>• Validation: all fields required.<br>• Data persisted to `business_goals` table.<br>• Success message and redirect to “Review Goals” page. |
| **1.2** | **As a** business stakeholder, **I want** to attach supporting documents (e.g., cost reports, compliance docs) **so that** the migration team has context. | • File upload widget (PDF, DOCX, XLSX, max 10 MB).<br>• File stored in S3 bucket with unique key.<br>• Metadata stored in `goal_documents` table linked to goal ID.<br>• List view shows file name, size, upload date. |
| **1.3** | **As a** business stakeholder, **I want** to view a consolidated dashboard of all business goals **so that** I can track progress. | • Dashboard page lists goals with KPI status (green/yellow/red).<br>• Filter by status, priority, deadline.<br>• Export to CSV button. |

---

## Epic 2 – Inventory Existing Infrastructure

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **2.1** | **As a** system administrator, **I want** to import an inventory of on‑prem servers, databases, and applications **so that** the tool knows what needs to move. | • CSV upload with columns: `name`, `type`, `OS`, `CPU`, `RAM`, `Storage`, `IP`, `AppDependencies`.<br>• Validation: required columns present, data types correct.<br>• Parsed rows stored in `inventory` table.<br>• Duplicate detection with warning. |
| **2.2** | **As a** system administrator, **I want** to run a live discovery scan via API **so that** the inventory stays up‑to‑date. | • “Run Scan” button triggers async job.<br>• Job polls target hosts (HTTPS/SSH) for system facts.<br>• Results merged into `inventory` table.<br>• Job status page shows progress and errors. |
| **2.3** | **As a** system administrator, **I want** to view a topology map of the current environment **so that** I can spot dependencies. | • Graph view (D3.js) showing nodes (servers, DBs, apps) and edges (calls, data flows).<br>• Hover shows details.<br>• Export to PNG. |

---

## Epic 3 – Define Cloud Target Architecture

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **3.1** | **As a** cloud architect, **I want** to select a target cloud provider (AWS, Azure, GCP) **so that** the migration plan uses provider‑specific services. | • Dropdown list of providers.<br>• Provider selection stored in `migration_plan` table.<br>• UI updates to show provider‑specific options. |
| **3.2** | **As a** cloud architect, **I want** to map on‑prem workloads to target services (e.g., EC2, RDS, GKE) **so that** the plan reflects realistic deployment options. | • Drag‑and‑drop interface: inventory items → target service cards.<br>• Validation: incompatible mappings flagged.<br>• Mapping saved to `workload_mappings` table. |
| **3.3** | **As a** cloud architect, **I want** to specify network topology (VPC, subnets, peering) **so that** security and connectivity are planned. | • Network editor with subnet blocks.<br>• Validation: CIDR overlap checks.<br>• Data stored in `network_plan` table. |

---

## Epic 4 – Generate Migration Roadmap

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **4.1** | **As a** project manager, **I want** the tool to auto‑generate a phased migration schedule **so that** I can allocate resources. | • Algorithm creates phases (pilot, bulk, cut‑over) based on dependencies.<br>• Output table with phase, start/end dates, tasks.<br>• Export to Gantt chart (PNG/Excel). |
| **4.2** | **As a** project manager, **I want** to adjust the schedule manually **so that** I can accommodate business constraints. | • Inline editing of dates and task order.<br>• Conflict detection (overlap, resource limits).<br>• Save changes to `migration_schedule` table. |
| **4.3** | **As a** project manager, **I want** to see risk scores for each phase **so that** I can prioritize mitigation. | • Risk score calculated from workload criticality, dependency count, and provider SLA.<br>• Color‑coded risk bar on schedule view.<br>• Export risk report. |

---

## Epic 5 – Cost Estimation & Optimization

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **5.1** | **As a** finance analyst, **I want** to estimate monthly cloud spend **so that** I can compare against on‑prem costs. | • Integration with provider pricing APIs.<br>• Calculates cost per workload, total, and savings.<br>• Results displayed in a cost dashboard. |
| **5.2** | **As a** finance analyst, **I want** to apply discount models (Reserved Instances, Savings Plans) **so that** the estimate is realistic. | • UI to select discount type and term.<br>• Re‑calculation updates cost view.<br>• Option to export cost model. |
| **5.3** | **As a** finance analyst, **I want** to generate a cost‑benefit report **so that** stakeholders can approve the migration. | • PDF report with charts (cost over time, savings, ROI).<br>• Includes assumptions and sensitivity analysis.<br>• Email send‑to list. |

---

## Epic 6 – Validation & Compliance Checks

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **6.1** | **As a** compliance officer, **I want** the tool to flag regulatory gaps (e.g., GDPR, HIPAA) **so that** we avoid legal issues. | • Rule engine checks mapping against compliance matrix.<br>• Highlights gaps in a compliance report.<br>• Export to PDF. |
| **6.2** | **As a** security engineer, **I want** to run automated security scans on target architecture **so that** we ensure baseline security. | • Trigger scan via provider security APIs (e.g., AWS Config).<br>• Results stored in `security_report` table.<br>• Dashboard shows findings with severity. |
| **6.3** | **As a** compliance officer, **I want** to approve or reject the plan **so that** only compliant migrations proceed. | • Approval button on final plan page.<br>• Approval status stored in `migration_plan`.<br>• Audit log of approver and timestamp. |

---

## Epic 7 – Execution & Monitoring

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **7.1** | **As a** DevOps engineer, **I want** to trigger automated deployment scripts **so that** the migration can be executed without manual effort. | • “Deploy” button per phase.<br>• Executes Terraform/CloudFormation templates.<br>• Logs stored in `deployment_logs`. |
| **7.2** | **As a** DevOps engineer, **I want** real‑time monitoring of migration progress **so that** I can react to failures. | • Live status feed (WebSocket) showing task completion.<br>• Alerts on failures (email/SMS). |
| **7.3** | **As a** DevOps engineer, **I want** to rollback a phase if needed **so that** we minimize downtime. | • Rollback button per phase.<br>• Executes provider rollback scripts.<br>• Confirmation dialog with risk warning. |

---

## Epic 8 – Documentation & Knowledge Capture

| # | User Story | Acceptance Criteria |
|---|-------------|---------------------|
| **8.1** | **As a** technical writer, **I want** the tool to auto‑generate migration documentation **so that** the team has up‑to‑date reference. | • Generates Markdown/HTML docs covering architecture, scripts, and runbooks.<br>• Stored in `docs` bucket.<br>• Link to docs on migration plan page. |
| **8.2** | **As a** technical writer, **I want** to annotate the docs with comments **so that** future teams can understand decisions. | • Inline comment system tied to doc sections.<br>• Comments stored in `doc_comments` table.<br>• Threaded view. |
| **8.3** | **As a** technical writer, **I want** to export the entire documentation set as a ZIP **so that** it can be archived. | • Export button triggers ZIP of all docs and comments.<br>• Download link provided. |

---

## MVP Release Order

1. **Epic 1** – Capture Business Objectives  
2. **Epic 2** – Inventory Existing Infrastructure  
3. **Epic 3** – Define Cloud Target Architecture  
4. **Epic 4** – Generate Migration Roadmap  
5. **Epic 5** – Cost Estimation & Optimization  
6. **Epic 6** – Validation & Compliance Checks  
7. **Epic 7** – Execution & Monitoring  
8. **Epic 8** – Documentation & Knowledge Capture  

> **Note**: Each epic builds on the previous one; early epics provide data models and UI scaffolding that later epics consume. The MVP focuses on Epics 1‑4, delivering a fully functional planning tool. Subsequent releases will add cost, compliance, execution, and documentation features.
