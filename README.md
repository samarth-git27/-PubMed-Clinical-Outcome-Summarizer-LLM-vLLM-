🚀 PubMed Clinical Outcome Summarizer (LLM + vLLM)

This project implements a fault-tolerant data processing pipeline that ingests messy PubMed-style JSON data and generates one-line clinical outcome summaries using a locally hosted Llama 3.3 70B model via vLLM
📌 Overview

This project implements a fault-tolerant data processing pipeline that ingests messy PubMed-style JSON data and generates one-line clinical outcome summaries using a locally hosted Llama 3.3 70B model via vLLM.

The system is designed with a strong focus on:

Data robustness (handling inconsistent schemas)
Reliability under failure conditions
Infrastructure-aware deployment
🎯 Key Features
🧹 Data Normalization & Cleaning
Handles inconsistent JSON structures (ArticleTitle vs title, abstract_text vs Abstract)
Skips corrupted or incomplete entries (e.g., missing abstracts)
Normalizes author formats into a consistent schema
🤖 LLM Integration (vLLM)
OpenAI-compatible API interaction with locally hosted LLM
Prompt engineered for single-sentence clinical outcome summarization
Low temperature (0.2) for deterministic outputs
⚡ Fault Tolerance & Reliability
Configurable request timeout (50 seconds) to support slow inference
Automatic retry mechanism (3 attempts) for transient failures
Graceful fallback response when LLM is unavailable
Pipeline continues processing even after failures
📊 Observability (Advanced)
Logs LLM response latency for performance monitoring
Structured logging for debugging and traceability
🧠 Infrastructure-Aware Design
Optimized vLLM configuration for Llama 70B
Prevents GPU Out-Of-Memory (OOM) using:
Tensor parallelism
Controlled GPU memory utilization
Reduced sequence length
🏗️ Project Structure
pubmed-llm-pipeline/
│
├── pubmed_summarizer.py     # Core pipeline logic
├── run_vllm.sh              # vLLM server startup script
├── docker-compose.yml       # Optional container orchestration
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
⚙️ Setup & Installation
1️⃣ Clone the Repository
git clone <your-repo-link>
cd pubmed-llm-pipeline
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate   # Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
🚀 Running the System
🔹 Step 1: Start LLM Server (DGX / GPU System)
chmod +x run_vllm.sh
./run_vllm.sh
🔹 Step 2: Run Pipeline
python pubmed_summarizer.py
🧪 Example Output
ID: PMID:349281
Title: Efficacy of Drug X in severe cardiac failure.
Summary: ERROR: Unable to get response from LLM

Note: If the LLM server is unavailable, the system gracefully handles failures using retries and fallback responses.

⚠️ Handling Real-World Failures
Scenario	Behavior
Missing abstract	Entry skipped
Slow server (45s delay)	Handled via timeout (50s)
Connection failure	Retries triggered
Server unavailable	Safe fallback returned
Partial failure	Pipeline continues
🐳 vLLM Deployment (OOM-Safe Configuration)
docker run --gpus all \
  --runtime=nvidia \
  --ipc=host \
  --network=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.3-70B-Instruct \
  --tensor-parallel-size 8 \
  --gpu-memory-utilization 0.85 \
  --max-model-len 4096 \
  --dtype float16 \
  --enforce-eager
🎥 Walkthrough Video

📺 Unlisted YouTube Demo:
[PASTE YOUR LINK HERE]

🧠 Design Decisions
Skipping null abstracts avoids meaningless LLM calls
Retry + timeout ensures robustness under real-world latency
Latency logging improves observability
Infrastructure tuning prevents GPU crashes in large models
🔮 Future Improvements
Async batching for higher throughput
Caching repeated requests
Structured output validation
Integration with monitoring tools (Prometheus/Grafana)
📌 Conclusion

This project demonstrates not just functional correctness, but production-grade system design, focusing on:

Reliability
Scalability
Infrastructure awareness
👤 Author

Samarth J Bharadwaj
Final Year Engineering Student | Software Development | AI/ML
