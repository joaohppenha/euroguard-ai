# EuroGuard AI: RAG Compliance System for GDPR & EU AI Act

EuroGuard AI is an enterprise-grade Retrieval-Augmented Generation (RAG) application engineered to assist legal, tech, and compliance teams in navigating European digital regulations, specifically the **General Data Protection Regulation (GDPR)** and the **EU Artificial Intelligence Act (EU AI Act)**.

The application indexes regulatory framework articles using vector embeddings, stores them in a PostgreSQL database powered by `pgvector`, and provides grounded, hallucination-resistant answers via Google's `Gemini 3.6 Flash` model.

---

## Executive Summary & "10x Solution" Impact

### 1. Zero-Hallucination Regulatory Grounding
Standard LLMs frequently hallucinate legal interpretations or confuse regulatory frameworks. EuroGuard AI solves this by strictly constraining prompt contexts to relevant vector chunks retrieved from PostgreSQL. If a user query falls outside the retrieved context, system guardrails prevent speculative answers.

### 2. High-Resilience API Strategy
To withstand LLM API rate limits, transient network outages, and 503 unavailability errors during peak demand, the backend utilizes `tenacity` retry logic with targeted exception filtering and fast backoffs, ensuring a seamless user experience without HTTP timeouts.

### 3. Containerized & Portable Infrastructure
By encapsulating the PostgreSQL `pgvector` database inside a Podman container environment (`docker-compose.yml` / `Containerfile`), the system achieves complete environment isolation, reproducible local setup, and seamless cloud migration capabilities.

---

## Architecture Overview

```text
+------------------+         HTTP/JSON         +-------------------+
|                  | ------------------------> |                   |
|  Streamlit UI    |                           |  FastAPI Backend  |
|  (Chat Frontend) | <------------------------ |  (REST Service)   |
+------------------+                           +-------------------+
                                                         |
                                             SQLAlchemy  |  pgvector
                                                         v
                                               +-------------------+
                                               |  PostgreSQL DB    |
                                               |  (Podman Engine)  |
                                               +-------------------+
                                                         |
                                              SDK Client | Embeddings / RAG
                                                         v
                                               +-------------------+
                                               |  Google Gemini    |
                                               |  3.6 Flash API    |
                                               +-------------------+
```

---

## Technical Stack & Key Tools

* **Backend Framework:** FastAPI (Python 3.x) with Pydantic for request/response validation and dependency injection.
* **Database & Vector Search:** PostgreSQL with the `pgvector` extension for efficient cosine similarity vector searches (`<=>`).
* **ORM & Database Management:** SQLAlchemy with session-scoped connection pooling.
* **Large Language Model (LLM):** Google GenAI SDK using `models/gemini-3.6-flash` for reasoning and `models/gemini-embedding-001` for vector embeddings.
* **Frontend Interface:** Streamlit chat application with custom state management and HTTP request handling (`requests`).
* **Containerization:** Podman & Podman Compose running PostgreSQL 16 on local port `5433`.
* **API Resilience:** `tenacity` library implementing exponential backoff and fixed retries to handle API rate limits and 503 errors seamlessly.
* **Environment & Security:** Sensitive credentials (API keys, connection strings) managed via `.env` files excluded from version control.

---

## Project Structure

```text
euroguard-ai/
├── app/
│   ├── core/
│   │   └── config.py         # Environment variables & settings
│   ├── db/
│   │   ├── session.py        # Database engine & session generator
│   │   └── init_db.py        # Extension & table initialization script
│   ├── models/
│   │   └── regulation.py     # SQLAlchemy ORM model for regulatory chunks
│   ├── schemas/
│   │   └── query.py          # Pydantic validation schemas
│   ├── services/
│   │   ├── llm.py            # Gemini API integration & tenacity retries
│   │   └── rag.py            # Vector retrieval & prompt construction
│   └── main.py               # FastAPI application routes & CORS
├── scripts/
│   └── seed_regulations.py   # Seeding script for GDPR & EU AI Act data
├── Containerfile             # Podman build configuration
├── docker-compose.yml        # Multi-container service definitions
├── streamlit_app.py          # Interactive web UI front-end
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## Getting Started

### Prerequisites

* **Python 3.10+**
* **Podman** (or Docker) & **Podman Compose**
* **Google Gemini API Key**

### 1. Database Setup with Podman

Start the PostgreSQL instance containing the `pgvector` extension:

```bash
podman-compose up -d
```

### 2. Virtual Environment & Dependencies

Create and activate a Python virtual environment, then install required packages:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://euroguard_user:euroguard_password@localhost:5433/euroguard_db
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Database Initialization & Seeding

Initialize the database schema and populate vector embeddings for GDPR and EU AI Act regulatory texts:

```bash
python -m app.db.init_db
python -m scripts.seed_regulations
```

---

## Execution & Workflow Validation

### Step 1: Local RAG Pipeline Validation
Before launching web servers, the retrieval mechanism and vector similarity search were validated directly via Python scripts.

![RAG Terminal Validation](testeRAG.jpg)

* **Explanation:** Validates vector generation via `gemini-embedding-001`, cosine similarity search against `pgvector`, and context injection into `gemini-3.6-flash`.

---

### Step 2: REST API Testing (Swagger UI)
The FastAPI backend exposes interactive OpenAPI documentation at `http://127.0.0.1:8000/docs`.

![Swagger UI Query Validation](testequery.jpg)

* **Explanation:** Validates the `POST /api/v1/query` endpoint. The endpoint receives a JSON payload, executes the database vector query, and returns structured responses with HTTP status `200 OK`.

---

### Step 3: Streamlit Web UI Execution
Start both services in separate terminal sessions:

```bash
# Terminal 1: FastAPI Backend
uvicorn app.main:app --reload

# Terminal 2: Streamlit Frontend
streamlit run streamlit_app.py
```

![Streamlit Interface Overview](interface.jpg)

* **Explanation:** Shows the Streamlit interface (`http://localhost:8501`) operating as an interactive chat application connected to the local FastAPI backend.

---

## Validation & Compliance Testing

### Test 1: GDPR Consent Conditions Validation
* **Query:** *"What are the key conditions for consent under GDPR?"*

![GDPR Test](t1.jpg)

* **Objective:** Verifies that the vector search accurately retrieves Article 6(1)(a) of the GDPR and that the LLM summarizes lawful processing conditions based strictly on the retrieved text.

---

### Test 2: EU AI Act High-Risk System Obligations
* **Query:** *"What are the data governance requirements for high-risk AI systems?"*

![EU AI Act Test](t2.jpg)

* **Objective:** Verifies retrieval precision for the EU AI Act framework (Article 10), checking that high-risk AI data management rules are properly extracted.

---

### Test 3: Out-of-Scope & Guardrail Enforcement
* **Query:** *"What is the capital of France?"*

![Out of Scope Test](t3.jpg)

* **Objective:** Tests system guardrails. Since the question is unrelated to European digital regulations, the system enforces prompt constraints and clearly states that the information is unavailable in the retrieved regulatory text, preventing AI hallucinations.

---

## Versioning & Git Setup

The project enforces strict separation of code and secrets using `.gitignore` (ignoring `.env`, `venv/`, `__pycache__/`, etc.).

All updates are versioned using conventional commits:
* **feat:** implementation of new features, routes, and UI elements.
* **fix:** exponential backoff retries and exception handlers.
* **docs:** inline code documentation and consolidated README.
* **test:** end-to-end pipeline and guardrail validation.
