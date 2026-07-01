
# RAG Complete Processing Pipeline Demo

A Python demo project that showcases a full **RAG (Retrieval-Augmented Generation)** workflow, from **document ingestion** to **intelligent question answering**.

This project demonstrates how to build an end-to-end RAG pipeline that includes:

- document ingestion
- intelligent chunking
- advanced retrieval
- context-based QA
- performance testing and monitoring

---

## Overview

This project is built around a demo class called `RAGPipelineComplete`, which uses `hello_agents.tools.RAGTool` to simulate the key stages of a real-world RAG system.

It is designed primarily as a **demo / learning / architecture illustration project**, rather than a production-ready implementation.

It is useful for:

- learning how a RAG system is structured
- demonstrating a complete RAG pipeline to a team
- prototyping an internal knowledge base assistant
- using as a starting point for document QA systems

---

## Features

### 1. Document Ingestion

The project demonstrates how to ingest multiple types of documents into a knowledge base.

Supported formats shown in the code include:

- PDF
- DOCX
- TXT
- MD
- HTML
- JSON

At the ingestion stage, the demo covers:

- multi-format text input
- document storage into the knowledge base
- `document_id` management
- metadata enrichment such as title, chapter, author, version, and timestamps
- batch document ingestion

---

### 2. Document Chunking

Chunking is one of the most important steps in a RAG system.  
This project demonstrates how long documents can be split into smaller units suitable for retrieval.

The code illustrates:

- semantic chunking
- chunking for structured documents
- the impact of chunking strategy on retrieval results
- balancing chunk size, context continuity, and retrieval quality

---

### 3. Advanced Retrieval

To improve recall and answer quality, the project demonstrates several retrieval enhancement strategies.

#### Multi-Query Expansion (MQE)
Expands a user query into multiple related search queries to improve retrieval coverage.

#### HyDE (Hypothetical Document Embeddings)
Generates a hypothetical answer first, then uses that generated content as the retrieval query.

#### Hybrid Retrieval
Breaks down a complex question into multiple sub-queries and combines the retrieved results.

#### Re-ranking
Reorders retrieved results using factors such as semantic relevance, freshness, and authority.

---

## Dependencies

Based on the code, the project depends on:

- Python 3
- `hello_agents.tools.RAGTool`
- `python-dotenv`

Example imports:

```python
from hello_agents.tools import RAGTool
from dotenv import load_dotenv
```
