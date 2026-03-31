<h1 align="center">🚀 PubMed Clinical Outcome Summarizer</h1>

<p align="center">
  <b>Fault-Tolerant LLM Pipeline using Llama 3.3 70B + vLLM</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LLM-Llama_3.3_70B-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Framework-vLLM-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge" />
</p>

---

## 🧠 Overview

This project implements a **fault-tolerant data processing pipeline** that ingests **messy PubMed JSON data** and generates **one-line clinical outcome summaries** using a locally hosted **Llama 3.3 70B model via vLLM**.

> Designed with a strong emphasis on **robustness, reliability, and infrastructure awareness**.

---

## ✨ Key Capabilities

### 🧹 Data Normalization
- Handles inconsistent schemas (`ArticleTitle` vs `title`, `abstract_text` vs `Abstract`)
- Skips corrupted or null entries safely
- Normalizes author formats into structured lists

---

### 🤖 LLM Integration
- OpenAI-compatible API with local vLLM server
- Prompt engineered for **concise clinical summarization**
- Low temperature (`0.2`) for deterministic outputs

---

### ⚡ Reliability & Fault Tolerance
- ⏱️ Timeout handling (**50s**) for slow inference
- 🔁 Automatic retries (**3 attempts**) for resilience
- 🛑 Graceful fallback on failure (no crashes)
- 🔄 Pipeline continues even after partial failures

---

### 📊 Observability
- Logs **LLM response latency**
- Structured logging for debugging and monitoring

---

### 🧠 Infrastructure Awareness
- Optimized deployment for **70B parameter models**
- Prevents GPU OOM using:
  - Tensor parallelism
  - Controlled memory utilization
  - Reduced sequence length

---

## 🏗️ Project Architecture

```bash
pubmed-llm-pipeline/
│
├── pubmed_summarizer.py   # Core pipeline logic
├── run_vllm.sh            # LLM server startup script
├── docker-compose.yml     # Container orchestration
├── requirements.txt       # Dependencies
├── README.md              # Documentation

Samarth J Bharadwaj
Final Year Engineering Student | Software Development | AI/ML
