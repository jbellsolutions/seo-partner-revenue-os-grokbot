# A draft is one file

`requests/owner/<today>-<id>-<n>.item`, exactly this shape:

```
ITEM: <today>-<id>-<n>
ROLE: <your agent's role id>
TYPE: <the message type>
PERSON: <id from the people list>
WHY: <the true reason for this person>
---PAYLOAD---
TO: <one email, or one profile URL>
SUBJECT: <lower case, a few words>
TEXT:
<the message, signed with owner.md's signature>
---END---
```

Before drafting: `python3 repo/guards/scripts/suppression.py check "<email or profile>"`; held means skip. After: `python3 repo/convlog/gate.py drafted <file> --agent <role>`.

| Agent | Types |
|---|---|
| dream-100 | dream100_first_touch, dream100_follow_up |
| dream-500 | dream500_first_touch, dream500_follow_up |
| partners | partner_outreach, partner_follow_up |
| cold-email | cold_email |
| speaker | show_pitch, show_follow_up |
| sales-crm | reply, radar_opener, invitation, member_note, follow_up |
