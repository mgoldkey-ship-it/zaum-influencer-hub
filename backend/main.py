from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(
    title="ZAUM // Influencer Hub API",
    description="Операционный сервис управления размещениями у блогеров и расчёта юнит-экономики (CPM / eCPM)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")


class BloggerPlacement(BaseModel):
    id: int
    sku: str
    blogger: str
    platform: str
    budget_Category: str
    subscribers: int
    age_group: str
    geo: str
    stories_reach: int
    reels_views: int
    ad_cost: int
    product_cost: int
    format: str
    status: str
    date: str
    link: str
    comment: Optional[str] = ""
    cpm: Optional[float] = 0.0


def load_db() -> List[dict]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(items: List[dict]) -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def calc_cpm(ad_cost: int, stories_reach: int) -> float:
    if stories_reach <= 0:
        return 0.0
    return round((ad_cost / stories_reach) * 1000, 2)


@app.get("/")
def serve_spa():
    return FileResponse(INDEX_HTML)


@app.get("/api/bloggers", response_model=List[BloggerPlacement])
def list_bloggers(platform: Optional[str] = None, status: Optional[str] = None):
    items = load_db()
    if platform and platform != "all":
        items = [x for x in items if x["platform"] == platform]
    if status and status != "all":
        items = [x for x in items if x["status"] == status]
    return items


@app.get("/api/stats")
def get_unit_economics():
    items = load_db()
    ad_sum = sum(x["ad_cost"] for x in items)
    prod_sum = sum(x["product_cost"] for x in items)
    stories_sum = sum(x["stories_reach"] for x in items)
    reels_sum = sum(x["reels_views"] for x in items)
    return {
        "count": len(items),
        "ad_cost_total": ad_sum,
        "product_cost_total": prod_sum,
        "full_budget_total": ad_sum + prod_sum,
        "stories_reach_total": stories_sum,
        "reels_views_total": reels_sum,
        "avg_cpm_stories": calc_cpm(ad_sum, stories_sum),
        "avg_ecpm_reels": calc_cpm(ad_sum, reels_sum),
    }
