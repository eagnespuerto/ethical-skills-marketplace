---
name: fetch-rules
description: Use when about to fetch, download, scrape, crawl or query any external website, archive or API - by script, curl, WebFetch or browser - especially bulk or repeated requests, astronomy archives (MPC, JPL Horizons, IRSA, CADC, MAST, SBN), retrying after a 403, 429 or 503, or writing a download or long-running script. Also when the user says "fetch rules" or "be polite to the server".
---

# Fetch rules

The owner's house rules for pulling data from other people's servers. We are guests on these sites. Follow every rule, including for small jobs and one-off scripts.

## Before fetching

1. **Read `robots.txt`** at the site root (`https://<host>/robots.txt`) once per host per session. Follow its `Disallow` paths and any `Crawl-delay`. If the site has a published API or usage policy, follow that too. No `robots.txt` (404) means no stated rules there; the rules below still apply.
2. **Identify honestly.** Send this on every scripted request, and never pretend to be a browser:

   ```
   User-Agent: YOUR NAME (auto) you@example.org
   From: you@example.org
   ```

   Replace `YOUR NAME` and `you@example.org` with the name and contact address the owner has approved for this purpose. If they are still placeholders, ask the owner what to send before the first request. Do not use any other address of theirs.

## While fetching

| Response | What to do |
|----------|-----------|
| 429 or 503 | Stop all requests to that host. Wait about 2 minutes (longer if `Retry-After` says so), then retry once. If it fails again, double the wait. After 3 failed tries, stop and tell the owner. |
| 403 | Do not retry the script or change its user-agent. Stop and follow "On a 403" below. |
| Timeout or connection error | Same as 503: wait about 2 minutes before retrying. |

### On a 403

A 403 on a script often means the site blocks automated clients (Cloudflare and similar), not that the data is off limits. Check `robots.txt` and the site's terms first: if they disallow the path, stop there.

Otherwise, stop and give the owner the choice before fetching anything more:

1. **Owner downloads it themself.** List the exact URLs (or the page and what to click), the expected size, and the folder to save into. Then carry on from the saved files.
2. **Use the browser.** Fetch through a real browser session, at human pace, one page at a time. All other rules still apply (pause between requests, cache, 3 GB cap).

Always offer both, with option 1 first. Do not pick the browser route without the owner's answer, even if they chose it for another site or an earlier job. If the browser is also refused, or shows a CAPTCHA or login wall, stop: only option 1 is left.

- **Volume cap:** at most 3 GB from one source in one night. Estimate the total size before starting. If the job needs more, split it across nights and say so. Keep a running byte count in the script and stop at the cap.
- **Go gently:** one worker, a short pause between requests, and cache every response on disk so nothing is fetched twice.

## In scripts

- Print a progress line at every 10% of the work done (10%, 20%, ... 100%), with the count and bytes so far. Flush the output so it shows up live.
- Make the job resumable: skip files already on disk.

```python
import time, requests

HEADERS = {"User-Agent": "YOUR NAME (auto) you@example.org",   # set your own
           "From": "you@example.org"}
CAP = 3 * 1024**3          # 3 GB per source per night
WAIT = 120                 # seconds before a retry

def fetch(url, tries=3):
    wait = WAIT
    for _ in range(tries):
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.status_code == 403:
            raise SystemExit(f"403 from {url}: stopping, not retrying")
        if r.status_code in (429, 503):
            time.sleep(max(wait, int(r.headers.get("Retry-After", 0) or 0)))
            wait *= 2
            continue
        r.raise_for_status()
        return r.content
    raise SystemExit(f"{url}: still failing after {tries} tries, stopping")

total, step = 0, max(1, len(urls) // 10)
for i, url in enumerate(urls, 1):
    total += len(fetch(url))            # save to cache here
    if total > CAP:
        raise SystemExit("3 GB cap reached for this source tonight")
    if i % step == 0 or i == len(urls):
        print(f"{100 * i // len(urls)}% ({i}/{len(urls)}, {total / 1e6:.0f} MB)", flush=True)
    time.sleep(1)
```

## Common mistakes

- Retrying a 429/503 at once, or in a tight loop.
- Treating a 403 as a puzzle to solve (new user-agent, different mirror path), or switching to the browser without first offering the owner the option to download the files themself.
- Leaving the default `python-requests` or `curl` user-agent.
- Running several workers "because each one is slow".
- Counting the 3 GB per file or per script instead of per source per night.
- A long script that prints nothing until the end.
