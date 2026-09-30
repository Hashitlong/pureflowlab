# PureFlow Lab (pureflowlab.com)

**The HTML files in this folder are the source of truth.** Edit them directly. There is no build step.

- The old Markdown sources and `build_site.py` in the parent folder are stale and archived (`build_site.LEGACY.py`); don't use them.
- Netlify publishes this folder as-is (`netlify.toml`, publish = ".").
- Before every commit, run `python3 check.py`. It must print `OK`. It checks affiliate tags (`pureflowlab-20`) and `rel="sponsored"`, local links and images, JSON-LD validity, HTML balance, title length, canonicals, sitemap coverage, and banned phrases (testing claims, prices, etc.).
- Editorial rules: every product claim comes from the maker or the product listing and is attributed ("per the listing"). No testing claims, prices, star ratings or invented stats. See `../drafts/REWRITE-RULES.md` and `../drafts/amazon-facts-2026-09-30.md`.
- Contact: support@mooresvillemarketing.com
