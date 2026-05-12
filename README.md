# How to add/update worlds

- Add an `{apworld}.toml` file in the `index/` directory. The name of the file **MUST** match the apworld name. So for `A link to the Past` which apworld is `alttp`, you would create a file named `alttp.toml`.
- In the `toml` file, add a name, `name = "A Link to the Past"`. That name **MUST** match the world name. If you're unsure what that means, it's the name used in your YAML.
- If the `name` field is nondescriptive or "ugly", add a `display_name` field with a pretty name. This especially useful for manuals where the name is `Manual_{game}_{author}`. In that case, add a `display_name` with `"Manual: {game}"`.
- Add a `home` field if applicable. In order of preference, it should contain a link to the discord thread, the github repo, any other webpage where the apworld might live. If there's none (i.e you made this apworld and it's not publically available anywhere else, omit the field).
- If the world needs to be tagged specifically, add a `tags = [...]`, available tags are: `ad` to mark the world as being from the after dark server.
- Add a `[versions]` section, one version per line. It should look something like this: `"{version}" = { src }`. Read the following sections to understand what that means.

## Version

Each version **MUST** be valid [semver](https://semver.org/). It doesn't matter if the apworld doesn't respect semver or doesn't even have a version that would be valid. We use this to make sure versions can be ordered.
If necessary, be creative with your version number.

For example, if an apworld has a release for a version `0.8`, you'd specify version `0.8.0` as the version the index.
If an apworld doesn't specify a version, as is usually the case with manuals, invent one. I tend to count the number of releases in the discord channel and name it `0.0.X`.
It's not always feasible though because of discord UX choices regarding search. It's fine to just go with `0.0.1`. When updating those apworlds, just increment the version number.

## Src

The index supports two different source types, `url` and `local`.
Since we're no longer accepting local sources, always use `url`.

Examples:

- The apworld is released on github and has a direct download link to the apworld in the release:
  `"0.1.0" = { url = "https://github.com/foo/bar/releases/download/0.1.0/foo.apworld" }`

### Special case for `url` releases

When the author uses tags that are semver compatible, it's possible to add a `default_url` field instead in the global scope of the toml like this:
`default_url = "https://github.com/foo/bar/releases/download/{{version}}/foo.apworld` and to specify versions like this: `"0.1.0" = {}`.
This makes it easier to update and can be used to automatically fetch newer versions so it's the prefered way of doing things.


# Criteria for inclusion

> [!IMPORTANT]
> Do **NOT** make demands of apworld authors to cater their apworlds for inclusion in this index.

- We will only accept apworlds that have a stable public URL: For example, a GitHub release artifact, or otherwise a direct link to the `.apworld` file. We will no longer accept apworlds directly into this repo (i.e. local sources).
- The apworld must not be banned on the Archipelago Discord server for copyright reasons.
- The apworld must not contain big unknown executable binary blobs or depend on any.
- The apworld must not contain obvious flaws that will make life difficult for anyone trying to generate large multiworlds. That includes direct usage of the random module, obvious logic flaws, forced interactivity during generation, or test failures that are deemed problematic.
- The apworld must not make any use of remote resources during generation. That includes checking the internet for the latest release or similar checks.
- The apworld must not require a ROM to generate. Apworlds already present in the index are exempt from this, but I will not accept any new ones.
- The generation failure rate calculated using Eijebong's [fuzzer](https://github.com/ionium-ap/Archipelago-fuzzer) must be below 1% (not counting `OptionError`s).
  - To help removing failures that would be considered restrictive starts, those rates will be calculated with a second [world](https://github.com/ionium-ap/empty-apworld) present that has 100 free locations. Any failures that remain may indicate a logic issue.
  - To help check for other logical issues that could prevent multiworlds from generating, we will also be checking against the following Fuzzer tests. These must fall within the 1% rule:
    - GERpocalypse, checks for issues with Generic Entrance Randomization (GER). See AP docs for more information:  [Entrance Rando](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/entrance%20randomization.md)
    - Indirect conditions, checks for issues related to indirect conditions, see AP docs for more information: [World FAQ](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld_dev_faq.md?plain=1#L101) or [World API](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#an-important-note-on-entrance-access-rules)
    - Item counts match the location count
    - Lambda variable capture issues (typically creates incorrect rule conditions)
    - Item/Location references match check (i.e. if Item A is on Location A, both of these should point to each other)
    - No stage output item/location changes (rogue behaviour, do not do this)
  - Some exceptions could be made for failures happening early during generation (before `generate_basic`) as those would most likely be detected by YAML validation and won't result in a big time loss during generation
- If the apworld is a beta for core verified game then it must have a different game name (`LADX` -> `LADX beta`)

- Note: Other Fuzzer tests may also be done on the world at the time of merging into the index, at the benefit of helping devs discover other types of bugs such as:
  - Universal Tracker compatibility issues
  - Determinism (i.e. that using the same random seed number and same input yaml(s) should produce the same outcome every single time)
