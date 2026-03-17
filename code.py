import subprocess
import system
import time

def updateGitTags(tag_provider="default", instance_name="GitInfo"):
    # Define the path to your Ignition project folder
    repo_path = "C:\Users\dshevchyk\Desktop\PersonalProjects\IgniteStrava\data\projects\StravaInIgnition"
    logger = system.util.getLogger("GitUtils")
    
    #UDT/Instance checker params
    base_provider = "[{}]".format(tag_provider)
    udt_name = "GitContext"
    udt_def_path = "{}_types_/{}".format(base_provider, udt_name)
    instance_path = "{}{}".format(base_provider, instance_name)
    
    #Check if exist, if not, create
    if not system.tag.exists(udt_def_path):
        logger.info("UDT Definition '{}' not found. Creating it...".format(udt_name))
        udt_def = {
            "name": udt_name,
            "tagType": "UdtType",
            "tags": [
                {"name": "Branch", "valueSource": "memory", "dataType": "String",
                "documentation": "The currently checked-out local branch", "toolTip": "The currently checked-out local branch"},
                {"name": "CommitHash", "valueSource": "memory", "dataType": "String",
                "documentation": "The short identifier of the currently running code", "toolTip": "The short identifier of the currently running code"},
                {"name": "CommitMessage", "valueSource": "memory", "dataType": "String",
                "documentation": "Last Commit Message", "toolTip": "Last Commit Message"},
                {"name": "Author", "valueSource": "memory", "dataType": "String",
                "documentation": "Author", "toolTip": "Author"},
                {"name": "LastUpdate", "valueSource": "memory", "dataType": "DateTime", 
                "documentation": "When the Ignition script last polled this data", "toolTip": "When the Ignition script last polled this data"},
                {"name": "IsDirty", "valueSource": "memory", "dataType": "Boolean",
                "documentation": "Is True if designer save is yet to be comitted", "toolTip": "Is True if designer save is yet to be comitted"},
                {"name": "LatestRelease", "valueSource": "memory", "dataType": "String",
                "documentation": "The most recent Git tag", "toolTip": "The most recent Git tag"},
                {"name": "CommitsBehind", "valueSource": "memory", "dataType": "Int4",
                "documentation": "How many commits the local branch is behind the local cache of the remote branch", "toolTip": "How many commits the local branch is behind the local cache of the remote branch"},
                {"name": "CommitDate", "valueSource": "memory", "dataType": "DateTime",
                "documentation": "Date and time of Commit currently being used", "toolTip": "Date and time of Commit currently being used"},
                {"name": "RemoteURL", "valueSource": "memory", "dataType": "String",
                "documentation": "Where the central repository is hosted.", "toolTip": "Where the central repository is hosted." }
            ]
        }
        system.tag.configure("{}_types_".format(base_provider), [udt_def], "m")
        
    if not system.tag.exists(instance_path):
        logger.info("UDT Instance '{}' not found. Creating it...".format(instance_name))
        udt_instance = {
            "name": instance_name,
            "typeId": udt_name,
            "tagType": "UdtInstance"
        }
        system.tag.configure(base_provider, [udt_instance], "m")
        
        time.sleep(0.5)

    def run_git_cmd(cmd):
        try:
            p = subprocess.Popen(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode == 0:
                return out.strip()
            else:
                logger.warn("Git command failed: {} | Error: {}".format(" ".join(cmd), err))
                return None
        except Exception as e:
            logger.error("Exception running Git: " + str(e))
            return None

    branch = run_git_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "Unknown"
    commit_hash = run_git_cmd(["git", "rev-parse", "--short", "HEAD"]) or "Unknown"
    commit_msg = run_git_cmd(["git", "log", "-1", "--pretty=%B"]) or "Unknown"
    author = run_git_cmd(["git", "log", "-1", "--pretty=%an"]) or "Unknown"
    status_out = run_git_cmd(["git", "status", "--porcelain"])
    is_dirty = True if status_out else False
    latest_release = run_git_cmd(["git", "describe", "--tags", "--abbrev=0"]) or "No Tags"
    behind_str = run_git_cmd(["git", "rev-list", "--count", "HEAD..@{u}"])
    commits_behind = int(behind_str) if behind_str and behind_str.isdigit() else 0
    commit_unix = run_git_cmd(["git", "log", "-1", "--format=%ct"])
    
    if commit_unix and commit_unix.isdigit():
        commit_date = system.date.fromMillis(int(commit_unix) * 1000)
    else:
        commit_date = None
        
    remote_url = run_git_cmd(["git", "config", "--get", "remote.origin.url"]) or "Unknown"

   #Write
    paths = [
        instance_path + "/Branch",
        instance_path + "/CommitHash",
        instance_path + "/CommitMessage",
        instance_path + "/Author",
        instance_path + "/LastUpdate",
        instance_path + "/IsDirty",
        instance_path + "/LatestRelease",
        instance_path + "/CommitsBehind",
        instance_path + "/CommitDate",
        instance_path + "/RemoteURL"
    ]
    
    values = [
        branch, commit_hash, commit_msg, author, 
        system.date.now(), is_dirty, latest_release, 
        commits_behind, commit_date, remote_url
    ]
    
    system.tag.writeBlocking(paths, values)
    logger.info("Git context tags updated successfully.")