"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Any normal matching query -- what matters is whether the item id in
        # session["selected_item"] matches what reached suggest_outfit and
        # create_fit_card. Criterion 3 -- state.
        "name": "item id carries through the session",
        "query": "90s track jacket in size M",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # A query that reliably finds one priced item -- checking whether the
        # fit card mentions the exact price. Criterion 4 -- the fit card.
        "name": "fit card mentions the price",
        "query": "leather boots under $60",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # A query with a price ceiling -- checking every returned listing is
        # at or under it. Criterion 5 -- the price filter.
        #
        # NOTE: criterion 5 was originally written as "5 queries with
        # different max_price values", but run_eval.py tests one scenario
        # across 5 tries of the SAME query, not 5 different ones. I revised
        # the criterion in criteria.md to fit this tooling -- see the note
        # there.
        "name": "price ceiling is respected",
        "query": "graphic tee under $25",
        "wardrobe": "example",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
