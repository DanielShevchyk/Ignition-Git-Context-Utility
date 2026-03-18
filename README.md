# Ignition-Git-Context-Utility
Python scripting utility for Ignition 8. It queries the local .git repo of a specified Ignition project using the subprocess library and writes the results to a UDT instance.

Context

Branch: The currently checked-out local branch

CommitHash: The short identifier of the currently running code.

CommitMessage & Author: Context on the last change applied to the server.

CommitDate: The actual age of the code running on the server.

IsDirty: A boolean that turns True if someone has made changes in the Ignition Designer and saved them to the Gateway, but hasn't committed those changes to Git yet.

LatestRelease: The most recent Git tag.

RemoteURL: Where the central repository is hosted.

LastUpdate: When the Ignition script last polled this data.

CommitsBehind: How many commits the local branch is behind the local cache of the remote branch.

Example of instance created:

<img width="700" height="271" alt="image" src="https://github.com/user-attachments/assets/69786ff3-c0cd-47d4-80b9-a0de2d40d24e" />
