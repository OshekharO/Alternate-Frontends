## 2024-09-11 - Dynamic Announcer and Keyboard Shortcuts in Single-Page Directory

**Learning:** In client-side filtered directories loaded dynamically via JSON, screen readers do not automatically announce search filtering updates or external link contexts. Additionally, missing focus-visible styling can make keyboard navigation invisible when default browser outlines are overridden.

**Action:** Added a debounced `aria-live="polite"` region (`#searchAnnouncer`) to communicate filtered counts, added `.sr-only` context tags `(opens in a new tab)` on external links, added `/` keyboard shortcut for rapid search access, and ensured explicit `focus-visible:ring-2` focus rings across all interactive elements.
