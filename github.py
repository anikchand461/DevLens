import base64
from urllib.parse import quote

import requests

from config import BASE_URL, HEADERS


def github_get(endpoint, params=None):

    response = requests.get(
        BASE_URL + endpoint,
        headers=HEADERS,
        params=params
    )

    response.raise_for_status()

    return response.json()


# ---------------- Repository ---------------- #

def get_repo(owner, repo):

    return github_get(
        f"/repos/{owner}/{repo}"
    )


# ---------------- Branches ---------------- #

def get_branches(owner, repo):

    return github_get(
        f"/repos/{owner}/{repo}/branches"
    )


def get_default_branch(owner, repo):

    repo_data = get_repo(owner, repo)

    return repo_data["default_branch"]


# ---------------- Tree ---------------- #

def get_tree(owner, repo, branch=None):

    if branch is None:
        branch = get_default_branch(owner, repo)

    branch = quote(branch, safe="")

    return github_get(
        f"/repos/{owner}/{repo}/git/trees/{branch}",
        {
            "recursive": 1
        }
    )["tree"]


# ---------------- File ---------------- #

def get_file(owner, repo, path, branch=None):

    path = quote(path, safe="/")

    params = {}

    if branch:
        params["ref"] = branch

    data = github_get(
        f"/repos/{owner}/{repo}/contents/{path}",
        params
    )

    if data.get("type") != "file":
        return None

    content = base64.b64decode(
        data["content"]
    ).decode(
        "utf-8",
        errors="ignore"
    )

    return {

        "path": path,

        "content": content

    }


# ---------------- All Files ---------------- #

SOURCE_EXTENSIONS = (

    ".py",

    ".js",

    ".ts",

    ".tsx",

    ".java",

    ".cpp",

    ".c",

    ".go",

    ".rs",

    ".php",

    ".html",

    ".css",

    ".json",

    ".md",

    ".yml",

    ".yaml"

)


def get_all_files(owner, repo, branch=None):

    tree = get_tree(owner, repo, branch)

    files = []

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        if path.endswith(SOURCE_EXTENSIONS):

            file = get_file(
                owner,
                repo,
                path,
                branch
            )

            if file:

                files.append(file)

    return files