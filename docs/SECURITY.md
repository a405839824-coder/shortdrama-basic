# Data and security

This is a local single-user stdio server. It has no HTTP listener, login system,
team roles or public download service. The connected client can read and edit
all basic-edition projects in the configured data directory. Do not share that
connection or directory with untrusted users.

Data is stored in an ordinary local SQLite database without application-level
encryption. Use your operating system's access controls and backup facilities.
The model client can receive source text through tools and has its own data policy.

Tool inputs are validated, source IDs are scoped to projects, and conflicting
edits are rejected. Excel export stores user strings as literal cells, including
strings that look like formulas. These checks do not establish content quality.

The release packager uses a fixed public-file list, rejects linked input paths,
and scans for some common credential patterns. This is a limited release check,
not a comprehensive security audit. Review any newly included files.

No private reporting channel has been established for this unpublished candidate.
When a public repository is created, use GitHub private vulnerability reporting
if enabled. Otherwise ask for a private contact without placing sensitive details
in a public issue. Report the version, a synthetic reproduction, and the impact.
