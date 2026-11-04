from backend.main import calc_cpm, get_unit_economics, list_bloggers

def test_cpm_formula_matches_sheet():
    # Row 2 from sheet: ad_cost=6300, stories_reach=3200 -> 1968.75
    assert calc_cpm(6300, 3200) == 1968.75
    assert calc_cpm(5000, 0) == 0.0

def test_bloggers_loaded():
    items = list_bloggers()
    assert len(items) == 24
    assert items[0]["sku"] == "DEMO-102"

def test_unit_economics_summary():
    stats = get_unit_economics()
    assert stats["count"] == 24
    assert stats["ad_cost_total"] == 510000
    assert stats["product_cost_total"] == 33600
    assert stats["full_budget_total"] == 543600
