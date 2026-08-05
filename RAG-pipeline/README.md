
# RAG Pipeline

This project demonstrates how to build an end-to-end RAG pipeline that includes:

- document ingestion
- intelligent chunking
- advanced retrieval

---

## Overview

Built a modular retrieval-augmented generation pipeline covering document ingestion, parsing, chunking, embedding generation, vector indexing, retrieval, context assembly, and LLM-based question answering. 
Developed advanced query expansion and retrieval techniques, including Multi-Query Expansion and Hypothetical Document Embeddings, to increase retrieval recall for ambiguous and complex questions.

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
