"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Matched by exact token overlap, case-insensitive, after
                     splitting both strings on whitespace and "/" — see the
                     size-matching rule in README.md's Tool Inventory. This
                     avoids "s" in "us 9" or "l" in "xl" false matches.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        Returns an empty list when nothing matches — not None, not an
        exception.
    """
    listings = load_listings()

    def size_tokens(s: str) -> set[str]:
        return {tok.upper() for tok in re.split(r"[\s/]+", s.strip()) if tok}

    requested_size_tokens = size_tokens(size) if size else None

    scored = []
    for listing in listings:
        if max_price is not None and listing["price"] > max_price:
            continue

        if requested_size_tokens is not None:
            listing_size_tokens = size_tokens(listing.get("size", ""))
            if not requested_size_tokens & listing_size_tokens:
                continue

        haystack = " ".join([
            listing.get("title", ""),
            listing.get("description", ""),
            " ".join(listing.get("style_tags", [])),
        ]).lower()
        query_words = [w for w in re.split(r"\W+", description.lower()) if w]
        score = sum(1 for w in query_words if w in haystack)

        if score == 0:
            continue

        scored.append((score, listing))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  May be empty.

    Returns:
        A non-empty string with outfit suggestions. With an empty wardrobe,
        returns general styling advice instead of raising or returning "".
    """
    item_desc = (
        f"{new_item.get('title', 'this item')} "
        f"({new_item.get('category', 'unknown category')}, "
        f"colors: {', '.join(new_item.get('colors', []))})"
    )

    items = wardrobe.get("items", [])

    if not items:
        prompt = (
            f"Someone is considering buying this thrifted item: {item_desc}. "
            f"They don't have any wardrobe items on file yet. Give general "
            f"styling advice for this piece — what kinds of things it would "
            f"pair well with, in one or two short suggestions."
        )
    else:
        wardrobe_desc = "\n".join(
            f"- {w.get('name', 'item')} ({w.get('category', '')}, "
            f"colors: {', '.join(w.get('colors', []))})"
            for w in items
        )
        prompt = (
            f"Someone is considering buying this thrifted item: {item_desc}.\n\n"
            f"Here is their current wardrobe:\n{wardrobe_desc}\n\n"
            f"Suggest one or two specific outfits that combine this new item "
            f"with pieces they already own. Name the actual wardrobe pieces "
            f"by name."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption. If `outfit` is empty or whitespace,
        returns a descriptive message rather than raising.
    """
    if not outfit or not outfit.strip():
        title = new_item.get("title", "this item")
        return (
            f"No outfit suggestion was available for {title}, so there's "
            f"nothing to build a caption from yet."
        )

    title = new_item.get("title", "this item")
    raw_price = new_item.get("price")
    if isinstance(raw_price, (int, float)):
        price = f"{raw_price:.0f}" if raw_price == int(raw_price) else f"{raw_price:.2f}"
    else:
        price = "an unknown price"
    platform = new_item.get("platform", "an unknown platform")
    brand = new_item.get("brand")
    colors = ", ".join(new_item.get("colors", []))

    prompt = (
        f"Write a short social-media caption (two to four sentences) someone "
        f"would actually post about this thrifted find, not a product "
        f"description.\n\n"
        f"Item: {title}"
        f"{f' by {brand}' if brand else ''} (colors: {colors}), "
        f"${price} on {platform}.\n"
        f"Outfit idea: {outfit}\n\n"
        f"Mention the item, its price, and its platform once each. Be "
        f"specific about the vibe — don't just describe the item, sell the "
        f"feeling of wearing it."
    )

    return generate(prompt)
