<! -- REMOVE BEFORE SENDING -->

Running observations for final README:

brief says “two weeks,” changelog date is later

articleId in the webhook sample vs article_uuid in the changelog

enUS in the search sample vs en-US as the changelog’s example

    "Is enUS in the desription vs en-US in the script deliberate?" (wanted check to see if something that will break or just something I'm unfamiliar with)

C1 removal release (4.3) vs “supported through 4.4”

no stated way to tell whether you still use v1

breaking: true on C1 is unclear, since v1 remains supported. I followed the flag. 

C2 changes behavior immediately but is marked non-breaking; confirm what “breaking” means

AI I didn't immediately trust: 
    “How would admin identify which integrations call v1?” (Claude suggestion made assumptions that weren't stated)

    I made changes to training module that referenced the changelog id rather than the title, which is inconsistent with the external-facing part of the module

C2 marked non-breaking, but it changes behavior for existing tenants,unclear whether custom timeouts are kept

C6 doesn’t say whether the old payload stays available

C4 default: off is read as False by YAML (Norway), and audience terms (“prospect”) aren’t defined


"Fix the spacing on this yaml" (way faster than formatting by hand)

"Is the "partners" audience one that will understand "deprecated"? (Claude rephrased something and I wanted to ensure the change matched the audience)

Changed format of Claude edits to test; extracted script logic from __main__ guard into main() entry point 

Claude suggested script as part of training module for C6; audience includes developers, so might be unecessary. Unclear on meaning of 'partners', so I chose to write for a potentially less technical audience and made an extension with it instead. 

"Check my indentation on lines 22-45"

"Write a Python 3 script that reads changelog.yaml and writes customer release
notes to output/release_notes.md.

Input: a YAML file with product, release, release_date, and a list of changes. Each
change has id, title, type, breaking, audience, visibility, description, and optional
fields such as removal_release, feature_flag, and default.Do not include any changes with visibility: internal. Separate breaking changes from the rest. Each entry has a "###" title, then "Who this affects", "What changed", and "Action required", each on its own line separated by blank lines. Derive "Action required" from the change type, using a lookup table with a safe default for unknown types. If a required field is missing, stop with a clear error naming the entry. Adding a new entry to the YAML must not require editing the script or the output. keep it brief and pythonic. leave lots of notes"


<! -- REMOVE BEFORE SENDING -->