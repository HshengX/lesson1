"""
GitCode MCP 服务器
使用 FastMCP 将 GitHub API 客户端封装为 MCP 服务
"""
from fastmcp import FastMCP
from ..github.server import (
    search_repository_by_url,
    get_pull_requests_by_repo_id,
    get_pull_request_files_by_repo_id,
    get_commits_by_repo_id
)

# 创建 FastMCP 实例
mcp = FastMCP(name="gitcode")


@mcp.tool()
async def search_repository(
    repo_url: str,
    per_page: int = 30,
    page: int = 1,
    sort: str = "stars",
    order: str = "desc"
) -> dict:
    """
    通过仓库地址模糊查找仓库信息
    
    Args:
        repo_url: 仓库地址，支持以下格式：
            - 完整 URL: https://github.com/owner/repo
            - GitHub URL: github.com/owner/repo
            - 简短格式: owner/repo
            - 仓库名称: repo (会进行模糊搜索)
        per_page: 每页返回数量，默认 30
        page: 页码，默认 1
        sort: 排序方式，可选值: stars, forks, updated，默认 stars
        order: 排序顺序，可选值: desc, asc，默认 desc
    
    Returns:
        包含搜索结果和状态的字典
    """
    return await search_repository_by_url(
        repo_url=repo_url,
        per_page=per_page,
        page=page,
        sort=sort,
        order=order
    )


@mcp.tool()
async def get_pull_requests(
    repo_id: int,
    state: str = "open",
    per_page: int = 30,
    page: int = 1,
    sort: str = "created",
    direction: str = "desc"
) -> dict:
    """
    根据仓库 ID 获取该仓库的所有 Pull Requests
    
    Args:
        repo_id: 仓库 ID（整数）
        state: PR 状态，可选值: open, closed, all，默认 open
        per_page: 每页返回数量，默认 30
        page: 页码，默认 1
        sort: 排序方式，可选值: created, updated, popularity，默认 created
        direction: 排序顺序，可选值: asc, desc，默认 desc
    
    Returns:
        包含 Pull Requests 数据和状态的字典
    """
    return await get_pull_requests_by_repo_id(
        repo_id=repo_id,
        state=state,
        per_page=per_page,
        page=page,
        sort=sort,
        direction=direction
    )


@mcp.tool()
async def get_pull_request_files(
    repo_id: int,
    pr_number: int
) -> dict:
    """
    根据仓库 ID 和 Pull Request 编号获取变更文件和变更内容
    
    Args:
        repo_id: 仓库 ID（整数）
        pr_number: Pull Request 编号（整数）
    
    Returns:
        包含变更文件数据和状态的字典
    """
    return await get_pull_request_files_by_repo_id(
        repo_id=repo_id,
        pr_number=pr_number
    )


@mcp.tool()
async def get_commits(
    repo_id: int,
    sha: str | None = None,
    path: str | None = None,
    author: str | None = None,
    since: str | None = None,
    until: str | None = None,
    per_page: int = 30,
    page: int = 1
) -> dict:
    """
    根据仓库 ID 获取该仓库的所有提交（commits）
    
    Args:
        repo_id: 仓库 ID（整数）
        sha: 分支或提交 SHA，默认为默认分支
        path: 只返回包含指定路径的提交
        author: 只返回指定作者的提交（GitHub 用户名或邮箱）
        since: 只返回此日期之后的提交（ISO 8601 格式，如 2024-01-01T00:00:00Z）
        until: 只返回此日期之前的提交（ISO 8601 格式）
        per_page: 每页返回数量，默认 30，最大 100
        page: 页码，默认 1
    
    Returns:
        包含提交数据和状态的字典
    """
    return await get_commits_by_repo_id(
        repo_id=repo_id,
        sha=sha,
        path=path,
        author=author,
        since=since,
        until=until,
        per_page=per_page,
        page=page
    )


if __name__ == "__main__":
    # 运行 MCP 服务器
    mcp.run()

