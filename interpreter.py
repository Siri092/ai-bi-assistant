import json
import os
import re

SUPPORTED_INTENTS = {"total_revenue", "top_product", "monthly_trend", "top_region", "compare_months", "help"}

def interpret_question(question: str):
    """Use an LLM when configured; otherwise use a safe local intent interpreter."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content":
                     "Classify the user's sales analytics question. Return JSON only with keys intent, month1, month2. "
                     "Allowed intent values: total_revenue, top_product, monthly_trend, top_region, compare_months, help. "
                     "Never produce SQL. For compare_months extract months as YYYY-MM when possible. If unclear use help."},
                    {"role": "user", "content": question}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            intent = result.get("intent")
            if intent not in SUPPORTED_INTENTS:
                return _local_interpret(question)
            return {"intent": intent, "params": {
                "month1": result.get("month1"), "month2": result.get("month2")
            }, "method": "llm"}
        except Exception:
            # Keep the app usable if the key/model/network is unavailable.
            pass
    return _local_interpret(question)

def _local_interpret(question: str):
    q = question.lower()
    months = re.findall(r"\b20\d{2}-(?:0[1-9]|1[0-2])\b", q)
    if any(word in q for word in ["compare", "change between", "difference between", "versus", " vs "]):
        return {"intent": "compare_months", "params": {
            "month1": months[0] if len(months) > 0 else None,
            "month2": months[1] if len(months) > 1 else None
        }, "method": "local"}
    if "month" in q and any(word in q for word in ["trend", "monthly", "each month", "by month"]):
        intent = "monthly_trend"
    elif any(word in q for word in ["highest region", "top region", "region generated", "region has the highest", "best region"]):
        intent = "top_region"
    elif any(word in q for word in ["highest product", "top product", "product generated", "best-selling product", "best selling product"]):
        intent = "top_product"
    elif any(word in q for word in ["total revenue", "revenue overall", "overall revenue", "total sales"]):
        intent = "total_revenue"
    elif "revenue" in q and ("trend" in q or "monthly" in q):
        intent = "monthly_trend"
    else:
        intent = "help"
    return {"intent": intent, "params": {}, "method": "local"}
