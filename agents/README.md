# The functions, one folder and one chat each

Each of the nine has its own folder here and its own chat under the product's main chat. A folder holds `README.md` (what the function is and what it is built from), `STATUS.md` (where it stands and what the owner needs to say, written by its chat), and its deeper spec as it is worked out: `PROCESS.md`, a settings example, prompts, any script.

| Function | Folder | Chat |
|---|---|---|
| Dream 100 | [dream-100/](dream-100/README.md) | Revenue OS · Dream 100 |
| Dream 500 | [dream-500/](dream-500/README.md) | Revenue OS · Dream 500 |
| Partners, collaborators and influencers | [partners/](partners/README.md) | Revenue OS · Partners, Collabs, Influencers |
| Cold email | [cold-email/](cold-email/README.md) | Revenue OS · Cold Leads |
| Lead Radar | [lead-radar/](lead-radar/README.md) | Revenue OS · Lead Radar |
| Content | [content/](content/README.md) | Revenue OS · Content |
| Podcast SpeakerAgent | [speaker/](speaker/README.md) | Revenue OS · SpeakerAgent |
| AEO and SEO | [aeo-seo/](aeo-seo/README.md) | Revenue OS · AEO SEO |
| Sales agent (replies and the CRM) | [sales-crm/](sales-crm/README.md) | Revenue OS · Sales Agent |


## How work flows

1. **The owner goes deeper in a function's chat.**
2. **Accepted work lands in the template through the main chat**: the function's branch is merged into the template's, and one line goes in [../CHANGELOG.md](../CHANGELOG.md) under that function, with a version.
3. **An application applies it from its own chat.** "Apply content 0.2 from the Revenue OS to this business, this way" works with no relay: the application's chat reads the changelog entry and the files it names ([../APPLY.md](../APPLY.md)).
