# OpenCone Product Descriptions

## 100-WORD VERSIONS

### Layman's (100 words)

OpenCone reads your documents and answers questions about them. Import PDFs, Word files, images, or code. The app extracts the text, stores it, and lets you search using natural language.

Ask "What did the contract say about termination?" and get an answer with sources. Answers stream in real-time. Optional tools generate charts or pull information from the web.

Supports PDFs, Word docs, images (reads text via OCR), Markdown, JSON, CSV, HTML, and code files. You provide your own OpenAI and Pinecone API keys—no subscription. Processing happens on your device. Data goes only to your connected accounts.

---

### Balanced (100 words)

OpenCone is a document search app that uses vector embeddings and AI to answer questions from your files. Import PDFs, DOCX, images, code, and 12 other formats. Text extraction runs locally; images use OCR.

Search modes: semantic similarity, hybrid (keyword + semantic), and two-stage reranking with BGE, Cohere, or Pinecone models. Answers stream from GPT-5.2, GPT-4o, or o-series models with source citations.

Code Interpreter generates charts and runs calculations. Web Search retrieves current information.

Bring your own OpenAI and Pinecone API keys. No subscription. On-device processing; vectors stored in your Pinecone account. For researchers, developers, and professionals.

---

### Technical (100 words)

iOS 17+ RAG client. 7-stage pipeline: security-scoped access → sandbox persistence → SHA256 deduplication → PDFKit/Vision OCR extraction → RecursiveTextSplitter chunking → OpenAI text-embedding-3-large (3072-dim, 50/batch) → Pinecone upsert with retry/circuit breaker.

Search: dense vector similarity, hybrid dense+sparse (alpha-weighted, dotproduct indexes), reranking (bge-reranker-v2-m3, cohere-rerank-3.5, pinecone-rerank-v0). SSE streaming via Responses API. GPT-5.2 with reasoning effort control (none/low/medium/high/xhigh).

Formats: PDF, DOCX, DOC, TXT, RTF, HTML, CSS, Markdown, JSON, XML, CSV, TSV, Python, JavaScript, PNG, JPEG, GIF, TIFF, BMP.

BYOK. Keychain-stored credentials. 100MB limit. 30s watchdog. Rate limiting. Structured logging.

---

## 300-WORD VERSIONS

### Layman's (300 words)

OpenCone lets you ask questions about your own documents and get real answers with sources.

**What it does:**
Import your files—PDFs, Word documents, images, text files, code, spreadsheets. The app reads them, including text in photos and scanned pages. Then you search by typing questions like "What are the payment terms?" or "Summarize the methodology section." The app finds relevant passages and generates an answer, showing exactly which documents it used.

**File types:**
PDF, Word (DOCX, DOC), plain text, RTF, HTML, Markdown, JSON, XML, CSV, Python, JavaScript, and images (PNG, JPEG, GIF, TIFF, BMP). Images are processed with text recognition.

**Search options:**
Regular search finds content by meaning. Hybrid search adds keyword matching. Precision mode runs results through a second filter for better accuracy.

**Features:**
Answers appear word-by-word as they generate. Code Interpreter creates charts and runs calculations when needed. Web Search pulls current information from the internet.

**Models:**
GPT-5.2, GPT-4o, and others. For reasoning models, you control how much thinking the AI does before answering.

**Privacy:**
The app reads your files on your device. Only the extracted text goes to OpenAI for processing. Vectors go to Pinecone for storage. No data goes anywhere else. No analytics or tracking.

**Pricing:**
You use your own OpenAI and Pinecone accounts. You pay those services directly based on usage. OpenCone has no subscription, no in-app purchases.

**Reliability:**
If API services fail, the app retries automatically. If failures continue, it stops trying temporarily to avoid wasting your API quota. File size limit is 100MB. Duplicate files are detected and skipped.

**Who uses it:**
Students, researchers, lawyers, developers, and anyone who needs to find information across many documents without reading them all.

---

### Balanced (300 words)

OpenCone is a retrieval-augmented generation (RAG) app for iOS that indexes your documents and answers questions using AI.

**Processing pipeline:**
Documents import via the system file picker. The app copies files to local storage with bookmark persistence. Duplicate detection uses SHA256 hashing. Text extraction runs locally—PDFKit for PDFs, Vision OCR for images. A recursive text splitter creates chunks respecting document structure. Chunks embed via OpenAI (text-embedding-3-large, 3072 dimensions, batches of 50). Vectors store in your Pinecone index.

**Search modes:**

1. Semantic search—finds similar content by vector distance
2. Hybrid search—combines dense vectors with sparse keyword vectors; alpha slider controls the mix
3. Reranking—applies a second model (BGE, Cohere, or Pinecone) to refine top results

Hybrid search requires a Pinecone index with dotproduct metric.

**Answer generation:**
Queries embed, retrieve top-k results, and pass to OpenAI's Responses API. Answers stream via SSE. Models include GPT-5.2 (400K context), GPT-4o, and o-series. Reasoning models support effort levels (none through max). Standard models use temperature and top-p.

**AI tools:**
Code Interpreter runs Python for charts, calculations, and data analysis. Web Search retrieves current information beyond your documents. Both are optional toggles.

**Supported formats:**
PDF, DOCX, DOC, TXT, RTF, HTML, CSS, Markdown, JSON, XML, CSV, TSV, Python, JavaScript, PNG, JPEG, GIF, TIFF, BMP.

**Data handling:**
On-device: file access, extraction, chunking, deduplication. Cloud: text chunks to OpenAI, vectors to Pinecone. No third-party analytics.

**Resilience:**
Retry logic with exponential backoff (3 attempts). Circuit breaker opens after 2 consecutive failures, resets after 20 seconds. Rate limiting at 100ms between requests. 30-second watchdog for stalled streams. 100MB file limit.

**Pricing:**
BYOK—bring your own API keys. No subscription.

**Audience:**
Researchers, legal professionals, developers, knowledge workers.

---

### Technical (300 words)

OpenCone implements a full RAG pipeline as a native SwiftUI application for iOS 17+ and macOS 14 Catalyst.

**Architecture:**
MVVM-S pattern with six services: OpenAIService, PineconeService, EmbeddingService, FileProcessorService, TextProcessorService, SpeechRecognitionService. Combine for reactive bindings. Swift async/await for concurrency.

**Ingestion pipeline (7 stages):**

1. Security-scoped resource access via DocumentPicker
2. Sandbox file copy with bookmark persistence
3. SHA256 content hash for deduplication
4. 100MB size limit enforcement
5. Text extraction: PDFKit (PDF), VNRecognizeTextRequest (images), raw read (text/code)
6. RecursiveTextSplitter with MIME-aware separators, configurable chunk size/overlap
7. OpenAI text-embedding-3-large (3072 dimensions, 50 chunks/batch) → Pinecone upsert

**Pinecone integration:**
Retry logic: 3 attempts with exponential backoff. Circuit breaker: opens after 2 consecutive failures, 20s reset. Rate limiting: 100ms minimum between requests. Host caching with 5-minute TTL. API versions: control plane 2024-07, data plane 2024-07, namespace 2025-10.

**Search modes:**

- Dense vector query (cosine, euclidean, dotproduct metrics)
- Hybrid query: weighted combination of dense + sparse vectors (alpha 0.0–1.0); requires dotproduct index
- Two-stage reranking: bge-reranker-v2-m3, cohere-rerank-3.5, pinecone-rerank-v0

**Completion:**
OpenAI Responses API with SSE streaming. Models: GPT-5.2 (400K context, 128K output), GPT-4o, GPT-4o-mini, o3, o1 series. Reasoning effort parameter (none/low/medium/high/xhigh) for GPT-5.x and o-series. Temperature/top-p for standard models.

**Tools:**
Code Interpreter (container: auto) with heuristic activation. Web Search with source extraction.

**Formats:**
PDF, DOCX, DOC, TXT, RTF, HTML, CSS, Markdown, JSON, XML, CSV, TSV, Python, JavaScript, PNG, JPEG, GIF, TIFF, BMP.

**Security:**
Keychain-stored credentials via SecureSettingsStore. Release build guard against bundled secrets. No third-party SDKs.

**Resilience:**
30s watchdog timer. Structured logging with export. Voice input via SFSpeechRecognizer.

BYOK model. No subscription.
