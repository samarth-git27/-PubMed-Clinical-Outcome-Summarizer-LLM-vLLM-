import json
import requests
import logging
from typing import List, Dict, Any

# -------------------- CONFIG --------------------
API_URL = "http://192.168.1.100:8000/v1/chat/completions"
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct"
REQUEST_TIMEOUT = 50  # Handles 45s delay safely
MAX_RETRIES = 3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------- RAW DATA --------------------
RAW_DATA = [
    {
        "id": "PMID:349281",
        "ArticleTitle": "Efficacy of Drug X in severe cardiac failure.",
        "abstract_text": "We tested 500 patients. The drug worked in 40% of cases but caused nausea.",
        "authorList": ["Smith, J", "Doe, A"]
    },
    {
        "id": 8829102,
        "title": None,
        "Abstract": "Null hypothesis rejected. No significant improvement noted in cohort B vs placebo.",
        "authors": "Unknown"
    },
    {
        "id": "ERR_NOT_FOUND",
        "ArticleTitle": "Corrupted Entry",
        "abstract_text": None
    }
]

# -------------------- DATA CLEANING --------------------
def clean_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    try:
        article_id = str(entry.get("id", "UNKNOWN"))

        title = (
            entry.get("ArticleTitle")
            or entry.get("title")
            or "No Title Available"
        )

        abstract = (
            entry.get("abstract_text")
            or entry.get("Abstract")
            or None
        )

        authors = (
            entry.get("authorList")
            or entry.get("authors")
            or []
        )

        if isinstance(authors, str):
            authors = [authors]

        if not abstract:
            logging.warning(f"Skipping {article_id}: Missing abstract")
            return None

        return {
            "id": article_id,
            "title": title,
            "abstract": abstract,
            "authors": authors
        }

    except Exception as e:
        logging.error(f"Corrupted entry skipped: {e}")
        return None


# -------------------- PAYLOAD --------------------
def build_payload(text: str) -> Dict[str, Any]:
    return {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the clinical outcome of this study in one sentence:\n{text}"
            }
        ],
        "temperature": 0.2,
        "max_tokens": 100
    }


# -------------------- API CALL --------------------
def call_llm(payload: Dict[str, Any]) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            logging.warning(f"Timeout (attempt {attempt + 1})... retrying")

        except requests.exceptions.ConnectionError:
            logging.warning(f"Connection error (attempt {attempt + 1})... retrying")

        except Exception as e:
            logging.error(f"Fatal error: {e}")
            break

    return "ERROR: Unable to get response from LLM"


# -------------------- MAIN --------------------
def main():
    cleaned_data: List[Dict[str, Any]] = []

    for entry in RAW_DATA:
        clean = clean_entry(entry)
        if clean:
            cleaned_data.append(clean)

    logging.info(f"Valid entries: {len(cleaned_data)}")

    for paper in cleaned_data:
        logging.info(f"Processing {paper['id']}")

        payload = build_payload(paper["abstract"])
        summary = call_llm(payload)

        print("\n----------------------------")
        print(f"ID: {paper['id']}")
        print(f"Title: {paper['title']}")
        print(f"Summary: {summary}")
        print("----------------------------\n")


if __name__ == "__main__":
    main()
