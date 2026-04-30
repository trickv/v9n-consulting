# Review AI Tools Landscape

Audit the AI tools landscape data in `just-do-ai/ai_tools_landscape.yaml` for accuracy, freshness, and completeness. This is a periodic review — propose changes but **always ask before making edits**.

## Data file

`just-do-ai/ai_tools_landscape.yaml` — YAML source of truth, rendered to HTML by `just-do-ai/build_landscape.py`.

## Step 0: Sync before researching

Before doing any research, run a `git pull` in the repo so the review starts from the latest version Patrick may have edited elsewhere.

## Step 1: Check every featured tool (full cards)

For each tool that has a full card (not just in the "more" list), fetch the tool's URL and verify:

1. **URL still works** — no 404s, no redirects to a different domain. If it redirects, note the new URL.
2. **Description is accurate** — compare against what the website actually says today. Flag anything that's changed (rebranding, new features, deprecated features, acquisitions).
3. **Pricing is current** — check pricing pages where available. Flag any changes. **Only list monthly subscription prices** — never annual/yearly prices, even when a vendor advertises an annual rate as their headline. If a tier is annual-only, convert to monthly equivalent or omit. This keeps cross-tool comparisons neutral and fair.
4. **Tool still exists** — flag any tools that have shut down, been acquired, or pivoted to something else entirely.

## Step 2: Check "more" list tools

For each tool in every `more:` list:

1. **URL still works** — fetch each URL from `more_urls:`. Flag 404s or redirects.
2. **Tool still exists and is relevant** — a quick check is fine here, no need for deep description verification.

## Step 3: Check for new tools to add

Search the web for new/emerging tools in each category:

- **Platform Builders** (prompt-to-app platforms)
- **Agentic Coding** (agent-first coding tools, CLI or otherwise)
- **AI-Native Editors** (IDE + AI tools)
- **AI Code Review** (automated PR review)
- **AI QA & Testing** (AI test automation)
- **Always-On Agents** (personal AI that runs 24/7)

Look for tools that:
- Have significant traction (GitHub stars, funding rounds, enterprise adoption)
- Are genuinely new (not already in the list)
- Fit clearly into one of the existing categories

## Step 4: Compile a change report

Present findings as a structured report to the user. For each proposed change, include:

### Format for corrections
```
**[Tool Name]** — [Category]
- Current: [what the YAML says now]
- Proposed: [what it should say]
- Source: [URL to the page/announcement that confirms the change]
```

### Format for new tool suggestions
```
**[Tool Name]** — suggest for [Category] ([card / more list])
- URL: [tool URL]
- What it does: [1-2 sentences]
- Why add it: [traction, funding, notable users, etc.]
- Source: [URL to the page/announcement]
```

### Format for removals
```
**[Tool Name]** — suggest removing from [Category]
- Reason: [shut down / acquired and absorbed / pivoted away / etc.]
- Source: [URL confirming this]
```

## Step 5: Wait for approval

**Do not edit files without explicit approval.** Present the full report and wait for the user to approve, modify, or reject each change.

## Step 6: Apply approved changes

Once approved:

1. Edit `just-do-ai/ai_tools_landscape.yaml` with the approved changes
2. Run `python3 just-do-ai/build_landscape.py` to regenerate the HTML
3. Show a summary of what was changed
4. Wait for the user to review and decide whether to commit and push

## Notes

- The YAML is the source of truth. Never edit the HTML directly.
- Tool descriptions should be concise (1-2 sentences) and factual, not marketing copy.
- Pricing in the `highlight` field should use approximate figures with `~` when exact pricing is complex.
- **Pricing is monthly-only.** Always list monthly subscription prices — never annual/yearly prices, even when the vendor's marketing leads with an annual rate. If a vendor only advertises annual pricing, divide by 12 and note "(billed annually)". This keeps comparisons across tools neutral and fair, since some vendors hide list price behind annual commitments.
- The `more_urls` dict must have an entry for every item in the `more` list.
- When a tool has been acqui-hired or acquired, note it in the description rather than removing the tool.
