from fastapi import FastAPI

from github import (
    get_repo,
    get_branches,
    get_tree,
    get_all_files
)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "RepoGPT API"
    }


# Repository


@app.get("/repo/{owner}/{repo}")
def repository(owner: str, repo: str):

    return get_repo(owner, repo)


# Branches


@app.get("/repo/{owner}/{repo}/branches")
def branches(owner: str, repo: str):

    return get_branches(owner, repo)


# Analyze Default Branch


@app.get("/analyze/{owner}/{repo}")
def analyze_default(
    owner: str,
    repo: str
):

    repo_info = get_repo(owner, repo)

    branch = repo_info["default_branch"]

    return {

        "repository": repo_info,

        "branch": branch,

        "tree": get_tree(
            owner,
            repo,
            branch
        ),

        "files": get_all_files(
            owner,
            repo,
            branch
        )

    }


# Analyze Specific Branch


@app.get("/analyze/{owner}/{repo}/{branch}")
def analyze_branch(
    owner: str,
    repo: str,
    branch: str
):

    repo_info = get_repo(owner, repo)

    return {

        "repository": repo_info,

        "branch": branch,

        "tree": get_tree(
            owner,
            repo,
            branch
        ),

        "files": get_all_files(
            owner,
            repo,
            branch
        )

    }